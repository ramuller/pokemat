import numpy as np
from PIL import Image
import cv2

class ScreenCapture:
    p = None
    def __init__(self, ts):
        self.ts = ts
        self.s = self.ts.specs
        
    def schow_image(self, img, title="picture", x=0, y=0, scale=1):
        cv2.imshow(title, img)
   
    def scan_image(self, x=0, y=0, w=0, h=0, channel="gray"):
        if w == 0:
            w = self.s['w']
        if h == 0:
            h = self.s['h']
            
        if channel == "gray":
            jbuf = self.ts.screen_capture_bw((x, y), (w, h), scale=False)
            pixel_array = np.array(jbuf["gray"], dtype=np.uint8).reshape((jbuf["height"], jbuf["width"]))
        else:
            jbuf = self.ts.screen_capture((x, y), (w, h), scale=False)
            rgb = self.yuv420_dict_to_rgb(jbuf)
            if channel == "red":
                pixel_array = np.array(rgb[:, :, 0], dtype=np.uint8).reshape(h-1, w-1)
            elif channel == "green":
                pixel_array = np.array(rgb[:, :, 0], dtype=np.uint8).reshape(h-1, w-1)
            elif channel == "blue":
                pixel_array = np.array(rgb[:, :, 0], dtype=np.uint8).reshape(h-1, w-1)
        return pixel_array
        return Image.fromarray(pixel_array, mode='L')
   
        
    def yuv420_dict_to_rgb(self, jbuf):
        w = jbuf["width"]
        h = jbuf["height"]  # use your real key here
    
        # Y plane (full resolution)
        Y = np.array(jbuf["gray"], dtype=np.uint8).reshape(h, w)
    
        # U, V planes (subsampled by 2 in both directions)
        U = np.array(jbuf["u"], dtype=np.uint8).reshape(h // 2, w // 2)
        V = np.array(jbuf["v"], dtype=np.uint8).reshape(h // 2, w // 2)
    
        # Upsample U and V to match Y
        U_full = cv2.resize(U, (w, h), interpolation=cv2.INTER_NEAREST).astype(np.float32)
        V_full = cv2.resize(V, (w, h), interpolation=cv2.INTER_NEAREST).astype(np.float32)
        Y_f    = Y.astype(np.float32)
    
        # YUV (BT.601) to RGB
        # R = Y + 1.402 * (V-128)
        # G = Y - 0.344136*(U-128) - 0.714136*(V-128)
        # B = Y + 1.772 * (U-128)
        d = U_full - 128.0
        e = V_full - 128.0
    
        R = Y_f + 1.402    * e
        G = Y_f - 0.344136 * d - 0.714136 * e
        B = Y_f + 1.772    * d
    
        # Clip and stack
        R = np.clip(R, 0, 255).astype(np.uint8)
        G = np.clip(G, 0, 255).astype(np.uint8)
        B = np.clip(B, 0, 255).astype(np.uint8)
    
        # Make RGB image (H, W, 3)
        rgb = np.stack([R, G, B], axis=-1)
        return rgb    