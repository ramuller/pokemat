import numpy as np
from PIL import Image
import cv2
from .structs import ScreenRegion

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
   
    def scan_region(self, reg : ScreenRegion):
        w = reg.xe - reg.xs + 1 
        h = reg.ye - reg.ys + 1
        x = reg.xs
        y = reg.ys
        try:
            if reg.color == "gray":
                jbuf = self.ts.write_to_phone(f"snip_gray:{x},{y},{w},{h}").json()
                pixel_array = np.array(jbuf["gray"], dtype=np.uint8).reshape((jbuf["height"], jbuf["width"]))
            else:
                jbuf = self.ts.screen_capture((x, y), (w, h), scale=False)
                if reg.color == "yuv":
                    g = np.array(jbuf["gray"], dtype=np.uint8).reshape(h, w)
                    u = np.array(jbuf["u"], dtype=np.uint8).reshape(h//2, w//2)
                    v = np.array(jbuf["v"], dtype=np.uint8).reshape(h//2, w//2)
                    pixel_array = (g, u ,v)
                else:
                    rgb = self.yuv420_dict_to_rgb(jbuf)
                    if reg.color == "red":
                        pixel_array = np.array(rgb[:, :, 0], dtype=np.uint8).reshape(h, w)
                    elif reg.color == "green":
                        pixel_array = np.array(rgb[:, :, 1], dtype=np.uint8).reshape(h, w)
                    elif reg.color == "blue":
                        pixel_array = np.array(rgb[:, :, 2], dtype=np.uint8).reshape(h, w)
                    elif reg.color == "rgb":
                        pixel_array = np.array(rgb, dtype=np.uint8).reshape(h, w, 3)
            return pixel_array
        except Exception as e:
            print(f'Exception {e}')
    
    
    def find_rgb(self, reg, r, g, b, tolerance = 20, verbose=0, wait=5):

        work_reg = reg
        data = work_reg.npa
        rl = r -tolerance
        ru = r + tolerance
        gl = g - tolerance
        gu = g + tolerance
        bl = b - tolerance
        bu = b + tolerance
  
        # Create masks for each channel
        red_mask = (data[..., 2] >= rl) & (data[..., 2] <= ru)
        green_mask = (data[..., 1] >= gl) & (data[..., 1] <= gu)
        blue_mask = (data[..., 0] >= bl) & (data[..., 0] <= bu)

        # Combine masks to find triplets satisfying all conditions
        combined_mask = red_mask & green_mask & blue_mask
        #  combined_mask = green_mask
        # Get the triplets (R, G, B) that fall within the specified ranges
        triplets_in_range = work_reg.npa[combined_mask]
        # print(f'len {len(triplets_in_range)}')
        ra = ~combined_mask
        # int_mask = ~combined_mask.astype(np.uint8) * 255
        int_mask = ra.astype(np.uint8) * 255

        if verbose >= 5:
            rm = red_mask.astype(np.uint8) * 255
            gm = green_mask.astype(np.uint8) * 255
            bm = blue_mask.astype(np.uint8) * 255
            rgb = np.hstack((rm, gm, bm))
            cv2.imshow('red', rgb)
            k = cv2.waitKey(wait)
            cv2.destroyAllWindows()       

        return int_mask
  
    def save_image(self, img, filename):
        im = Image.fromarray(img)
        im.save(filename)
        return
        
    def yuv420_dict_to_rgb(self, jbuf):
        W = jbuf["width"]
        H = jbuf["height"]  # use your real key here

        # Convert lists to arrays
        Y = np.array(jbuf["gray"], dtype=np.uint8).reshape(H, W)
        U = np.array(jbuf["u"], dtype=np.uint8).reshape(H // 2, W // 2)
        V = np.array(jbuf["v"], dtype=np.uint8).reshape(H // 2, W // 2)
        
        # Upsample U and V to full resolution
        U_up = cv2.resize(U, (W, H), interpolation=cv2.INTER_NEAREST)
        V_up = cv2.resize(V, (W, H), interpolation=cv2.INTER_NEAREST)

        # Merge into YUV image
        YUV = cv2.merge([Y, U_up, V_up])

        # Convert to BGR for display
        return cv2.cvtColor(YUV, cv2.COLOR_YUV2BGR)



    def yuv420_dict_to_rgb_old(self, jbuf):
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
        # rgb = np.stack([R, G, B], axis=-1)
        rgb = np.stack([B, G, R], axis=-1)
        return rgb

    def boxes_get(self, reg, verbose=0, pad=10):
        # self.ts.sc.show_image(img, wait=1000, title='unprocessed')
        reg.npa = cv2.normalize(reg.npa, None, 
                                alpha=0, beta=255, 
                                norm_type=cv2.NORM_MINMAX)
        
        candidates = []
        H, W = reg.npa.shape
        if verbose > 2:
                print(f'boxes NPA : H{H},W{W}')

        edges = cv2.Canny(reg.npa, 50, 150)
        if verbose > 9:
            cv2.imshow('boxes full area', reg.npa)
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

            if True: #True:  # hardcode debug
                tpad = 0
                cv2.imshow('current box',
                            reg.npa[
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
                xcs = x + pad
                xce = x + w - pad
                ycs = y + pad
                yce = y + h - pad
                br = ScreenRegion(reg.ts,
                                invert = reg.invert, 
                                process =reg.process,
                                xs=xcs, ys=ycs,
                                xe=xce, ye=yce)
                br.npa = reg.npa[ycs : yce, xcs : xce]

                boxes.append(br)
                # boxess.append({'rois': reg.npa[
                #     # y+pad : y+h-pad,
                #     ycs : yce,
                #     # x+pad : x+w-pad
                #     xcs : xce
                #     ],
                #     'x': xcs, 'y': ycs 
                #     })
                if verbose > 5:
                    self.ts.image.show_image(boxes[-1].npa, wait=1000, title='apended box')
        return boxes
    
    def process_array(self, reg, verbose=0):
        try:
            if reg.invert:
                reg.npa = cv2.bitwise_not(reg.npa)
            # if not reg.process:
            #     return reg
            reg.npa = cv2.normalize(reg.npa, 
                                None, 
                                alpha=0, beta=255, 
                                norm_type=cv2.NORM_MINMAX)
            if reg.threshold > 0:
                _, reg.npa = cv2.threshold(reg.npa, 
                    reg.threshold,
                    255, 
                    cv2.THRESH_BINARY
                    )
            elif reg.process:
                reg.npa = cv2.adaptiveThreshold(
                    reg.npa,
                    255,
                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                    cv2.THRESH_BINARY,
                    31,
                    5
                )
        except Exception as e:
            print(f'Exception in process_array {e}')
        return reg