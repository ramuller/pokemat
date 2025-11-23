# icon_detector.py
import cv2
import numpy as np
from dataclasses import dataclass

@dataclass
class Detection:
    icon_name: str
    score: float
    quad: np.ndarray  # 4x2 float array of corner points in the scene

class IconDetector:
    def __init__(self, icons: dict[str, np.ndarray], nfeatures: int = 1500):
        """
        icons: dict like {"save": icon_img, "print": icon_img, ...}
               images should be grayscale or BGR; will be converted to gray
        """
        self.orb = cv2.ORB_create(nfeatures=nfeatures, scaleFactor=1.2, nlevels=8)
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        self.db = {}
        for name, img in icons.items():
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if img.ndim == 3 else img
            kps, des = self.orb.detectAndCompute(gray, None)
            if des is None or len(kps) < 4:
                continue
            h, w = gray.shape[:2]
            self.db[name] = {"kps": kps, "des": des, "size": (w, h)}

    def detect(self, scene_img: np.ndarray, ratio=0.75, min_inliers=8, ransac_reproj_thresh=3.0) -> list[Detection]:
        gray_scene = cv2.cvtColor(scene_img, cv2.COLOR_BGR2GRAY) if scene_img.ndim == 3 else scene_img
        kps_s, des_s = self.orb.detectAndCompute(gray_scene, None)
        if des_s is None:
            return []

        detections = []
        for name, rec in self.db.items():
            matches = self._knn_match(rec["des"], des_s, k=2)
            good = []
            for m, n in matches:
                if m.distance < ratio * n.distance:
                    good.append(m)
            if len(good) < min_inliers:
                continue

            src_pts = np.float32([rec["kps"][m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kps_s[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
            H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, ransac_reproj_thresh)
            if H is None:
                continue

            inliers = int(mask.sum())
            if inliers < min_inliers:
                continue

            w, h = rec["size"]
            corners = np.float32([[0,0],[w,0],[w,h],[0,h]]).reshape(-1,1,2)
            proj = cv2.perspectiveTransform(corners, H).reshape(4,2)
            # simple score: inlier count (could normalize if needed)
            detections.append(Detection(icon_name=name, score=float(inliers), quad=proj))
        return detections

    def _knn_match(self, des1, des2, k=2):
        return self.bf.knnMatch(des1, des2, k=k)
