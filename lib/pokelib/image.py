import numpy as np
from PIL import Image
import cv2

class PokeImage:
    p = None
    def __init__(self, ts):
        self.ts = ts
        self.s = self.ts.specs
        
    def show_image(self, img, title="picture", x=0, y=0, scale=1, wait=0):
        try:
            cv2.imshow(title, img)
            k = cv2.waitKey(wait)
            cv2.destroyAllWindows()
            return k
        except Exception as e:
            print(e)       
   
    def scan_region(self, xs=0, ys=0, xe=0, ye=0, channel="gray"):
        if xe == 0 or xe > self.s['max_x']:
            xe = self.s['max_x']
        if ye == 0 or ye > self.s['max_y']:
            ye = self.s['max_y']
        if xs < 0:
            xs = 0
        if ys < 0:
            ys = 0
        w = xe - xs + 1 
        h = ye - ys + 1
        x = xs
        y = ys
        if channel == "gray":
            jbuf = self.ts.write_to_phone(f"snip_gray:{x},{y},{w},{h}").json()
            pixel_array = np.array(jbuf["gray"], dtype=np.uint8).reshape((jbuf["height"], jbuf["width"]))
        else:
            jbuf = self.ts.screen_capture((x, y), (w, h), scale=False)
            rgb = self.yuv420_dict_to_rgb(jbuf)
            if channel == "red":
                pixel_array = np.array(rgb[:, :, 0], dtype=np.uint8).reshape(h, w)
            elif channel == "green":
                pixel_array = np.array(rgb[:, :, 1], dtype=np.uint8).reshape(h, w)
            elif channel == "blue":
                pixel_array = np.array(rgb[:, :, 2], dtype=np.uint8).reshape(h, w)
        return pixel_array
        return Image.fromarray(pixel_array, mode='L')
   
    def save_image(self, img, filename):
        im = Image.fromarray(img)
        im.save(filename)
        return
        
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

    def boxes_get(self, npa, verbose=0, pad=10):
        # self.ts.sc.show_image(img, wait=1000, title='unprocessed')
        npa = cv2.normalize(npa, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        candidates = []
        H, W = npa.shape
        if verbose > 2:
                print(f'boxes NPA : H{H},W{W}')

        edges = cv2.Canny(npa, 50, 150)
        if verbose > 9:
            cv2.imshow('boxes full area', npa)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()
        contours, _ = cv2.findContours(
            edges,
            # cv2.RETR_EXTERNAL,
            cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE
            )
            
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            area = w * h
            # reject small stuff
            if area < 0.01 * W * H:
                continue
            
            if verbose > 2:
                print(f'Cont : x{x},y{y},w{w},h{h}')

            if False: #True:  # hardcode debug
                tpad = 0
                cv2.imshow('current box',
                            npa[
                                y+tpad : y+h-tpad,
                                x+tpad : x+w-tpad
                            ])
                cv2.waitKey(000)
                cv2.destroyAllWindows()
                            

            # reject near-fullscreen
            if area > 0.9 * W * H:
                continue
        
            # aspect ratio sanity
            aspect = w / float(h)
            # if 0.5 < aspect < 2.5: 
            if 0.5 < aspect < 20: 
                candidates.append((x, y, w, h))
            else:
                if verbose > 5:
                    print(f"Rejected box x{x},y{y},w{w},h{h} with aspect {aspect:.2f}") 
        unique = set(candidates)
        boxes = []
        if unique:
            for d in unique:
                x, y, w, h = d
                # clip area
                ycs = y + pad
                yce = y + h - pad
                xcs = x + pad
                xce = x + w - pad
                boxes.append({'rois': npa[
                    # y+pad : y+h-pad,
                    ycs : yce,
                    # x+pad : x+w-pad
                    xcs : xce
                    ],
                    'x': xcs, 'y': ycs 
                    })
                if verbose > 5:
                    self.ts.image.show_image(boxes[-1]['rois'], wait=1000, title='apended box')
        return boxes
    
    def process_array(self, npa, invert, process, verbose=0):
        try:
            if invert:
                npa = cv2.bitwise_not(npa)
            if not process:
                return npa
            npa = cv2.normalize(npa, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
            npa = cv2.adaptiveThreshold(
                npa,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                31,
                5
            )
        except Exception as e:
            print('e')
        return npa