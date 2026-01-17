# hybrid_icon_detector.py
import cv2
import numpy as np
from dataclasses import dataclass

@dataclass
class Detection:
    icon_name: str
    score: float
    quad: np.ndarray  # 4x2 float array of corner points in the scene

def _ensure_gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if img.ndim == 3 else img

def _nms(boxes, scores, iou_thr=0.3):
    if not boxes:
        return [], []
    idxs = np.argsort(scores)[::-1]
    keep = []
    boxes = np.array(boxes, dtype=np.float32)
    scores = np.array(scores, dtype=np.float32)
    while len(idxs) > 0:
        i = idxs[0]
        keep.append(i)
        xx1 = np.maximum(boxes[i,0], boxes[idxs[1:],0])
        yy1 = np.maximum(boxes[i,1], boxes[idxs[1:],1])
        xx2 = np.minimum(boxes[i,2], boxes[idxs[1:],2])
        yy2 = np.minimum(boxes[i,3], boxes[idxs[1:],3])
        w = np.maximum(0, xx2 - xx1)
        h = np.maximum(0, yy2 - yy1)
        inter = w * h
        area_i = (boxes[i,2]-boxes[i,0])*(boxes[i,3]-boxes[i,1])
        area_j = (boxes[idxs[1:],2]-boxes[idxs[1:],0])*(boxes[idxs[1:],3]-boxes[idxs[1:],1])
        iou = inter / (area_i + area_j - inter + 1e-9)
        idxs = idxs[1:][iou < iou_thr]
    return boxes[keep].tolist(), scores[keep].tolist()

class IconDetector:
    """
    Hybrid icon detector:
      - Uses ORB+RANSAC homography if the icon has features.
      - Falls back to multi-scale template matching for flat icons (like circles).
    """
    def __init__(self, icons: dict[str, np.ndarray], min_kp: int = 4):
        self.db = {}
        self.orb = cv2.ORB_create(nfeatures=2000, fastThreshold=5)
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)

        for name, img in icons.items():
            g = _ensure_gray(img)
            H, W = g.shape[:2]

            # Try ORB features
            kps, des = self.orb.detectAndCompute(g, None)
            if des is not None and len(kps) >= min_kp:
                self.db[name] = {
                    "mode": "orb",
                    "gray": g,
                    "kps": kps,
                    "des": des,
                    "size": (W, H),
                }
            else:
                # Template mode (also store inverted for light/dark UIs)
                self.db[name] = {
                    "mode": "template",
                    "tmpl": g,
                    "tmpl_inv": cv2.bitwise_not(g),
                    "size": (W, H),
                }

    def detect(
        self,
        scene_img: np.ndarray,
        *,
        ratio=0.75,
        min_inliers=8,
        ransac_reproj=3.0,
        # scales=np.linspace(0.8, 1.4, 15),
        scales=np.linspace(0.8, 1.3, 13),
        rotations=(0,),         # for templates; add (-10, 10) if needed
        thr=0.90,               # template score threshold (TM_CCOEFF_NORMED)
        max_candidates=200,     # per icon
        nms_iou=0.30
    ) -> list[Detection]:

        scene_gray = _ensure_gray(scene_img)

        # Compute scene features once (for ORB icons)
        kps_s, des_s = self.orb.detectAndCompute(scene_gray, None)

        detections: list[Detection] = []
        for name, rec in self.db.items():
            if rec["mode"] == "orb":
                if des_s is None:
                    continue
                matches = self.bf.knnMatch(rec["des"], des_s, k=2)
                good = [m for m, n in matches if m.distance < ratio * n.distance] if matches else []
                if len(good) < min_inliers:
                    continue
                src = np.float32([rec["kps"][m.queryIdx].pt for m in good]).reshape(-1,1,2)
                dst = np.float32([kps_s[m.trainIdx].pt for m in good]).reshape(-1,1,2)
                Hm, mask = cv2.findHomography(src, dst, cv2.RANSAC, ransac_reproj)
                if Hm is None or int(mask.sum()) < min_inliers:
                    continue
                W, H = rec["size"]
                corners = np.float32([[0,0],[W,0],[W,H],[0,H]]).reshape(-1,1,2)
                quad = cv2.perspectiveTransform(corners, Hm).reshape(4,2)
                detections.append(Detection(name, float(mask.sum()), quad))

            else:  # template mode
                tmpl0 = rec["tmpl"]
                boxes, scores = [], []

                def search_with_template(tmpl):
                    nonlocal boxes, scores
                    for ang in rotations:
                        # rotate template (if needed)
                        if ang != 0:
                            h, w = tmpl.shape
                            M = cv2.getRotationMatrix2D((w/2, h/2), ang, 1.0)
                            cos, sin = abs(M[0,0]), abs(M[0,1])
                            nW, nH = int((h*sin) + (w*cos)), int((h*cos) + (w*sin))
                            M[0,2] += (nW/2) - w/2
                            M[1,2] += (nH/2) - h/2
                            t_rot = cv2.warpAffine(tmpl, M, (nW, nH), flags=cv2.INTER_LINEAR, borderValue=0)
                        else:
                            t_rot = tmpl

                        for s in scales:
                            t = cv2.resize(t_rot, None, fx=s, fy=s, interpolation=cv2.INTER_LINEAR)
                            th, tw = t.shape[:2]
                            if th < 8 or tw < 8 or th >= scene_gray.shape[0] or tw >= scene_gray.shape[1]:
                                continue
                            res = cv2.matchTemplate(scene_gray, t, cv2.TM_CCOEFF_NORMED)
                            ys, xs = np.where(res >= thr)
                            for (y, x) in zip(ys, xs):
                                boxes.append((x, y, x+tw, y+th))
                                scores.append(float(res[y, x]))
                                if len(scores) >= max_candidates:
                                    return

                search_with_template(tmpl0)
                # also try inverted for light/dark mode differences
                if len(scores) < max_candidates:
                    search_with_template(rec["tmpl_inv"])

                if not boxes:
                    continue

                boxes, scores = _nms(boxes, scores, iou_thr=nms_iou)
                for score, (x1, y1, x2, y2) in zip(scores, boxes):
                    quad = np.array([[x1,y1],[x2,y1],[x2,y2],[x1,y2]], dtype=np.float32)
                    detections.append(Detection(name, float(score), quad))

        return detections
