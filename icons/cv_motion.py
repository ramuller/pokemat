import numpy as np
import cv2

class MotionDetectorRA:
    def __init__(self, alpha=0.05, thresh=25, min_area=500, morph_erode=1, morph_dilate=2):
        self.alpha = float(alpha)
        self.thresh = int(thresh)
        self.min_area = int(min_area)
        self.morph_erode = int(morph_erode)
        self.morph_dilate = int(morph_dilate)
        self._bg32f = None  # background model (float32, single-channel)

    def _prep_gray(self, frame):
        """Ensure single-channel 8-bit image."""
        if frame.ndim == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray = frame
        if gray.dtype != np.uint8:
            # if float in [0,1] or higher bit-depth -> scale/clip to 8-bit
            g = gray.astype(np.float32)
            g = np.clip(g, 0, 255)
            if g.max() <= 1.0:
                g = g * 255.0
            gray = g.astype(np.uint8)
        return gray

    def update(self, frame):
        """
        Input:
          frame: numpy array HxW or HxWx3
        Returns:
          mask: binary np.uint8 mask of motion (H x W, 0/255)
          boxes: list of (x, y, w, h) for detected moving regions
        """
        gray = self._prep_gray(frame)

        if self._bg32f is None:
            self._bg32f = gray.astype(np.float32)
            return np.zeros_like(gray, dtype=np.uint8), []

        # running average background
        cv2.accumulateWeighted(gray, self._bg32f, self.alpha)

        # |gray - background|
        bg8u = cv2.convertScaleAbs(self._bg32f)
        diff = cv2.absdiff(gray, bg8u)

        # threshold + morphology
        _, mask = cv2.threshold(diff, self.thresh, 255, cv2.THRESH_BINARY)
        if self.morph_erode > 0:
            mask = cv2.erode(mask, None, iterations=self.morph_erode)
        if self.morph_dilate > 0:
            mask = cv2.dilate(mask, None, iterations=self.morph_dilate)

        # contours -> bounding boxes
        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        boxes = []
        for c in contours:
            if cv2.contourArea(c) < self.min_area:
                continue
            x, y, w, h = cv2.boundingRect(c)
            boxes.append((x, y, w, h))
        return mask, boxes
