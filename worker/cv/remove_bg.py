import cv2 as cv
import numpy as np

def remove_bg3(img):
    canny = cv.Canny(img, 100, 150)
    
    kernel = np.ones((9,9), np.uint8)
    closing = cv.morphologyEx(canny, cv.MORPH_CLOSE, kernel)
    erosion = cv.erode(closing, cv.getStructuringElement(cv.MORPH_RECT, (3,3)))
    
    r=0; g=0; b=0; cnt=0
    h, w = img.shape[:2]

    for i in range(h):
        for j in range(w):
            if erosion[i, j] == 255:
                r += img.item(i,j,0)
                g += img.item(i,j,1)
                b += img.item(i,j,2)
                cnt += 1

    for i in range(h):
        for j in range(w):
            if erosion[i, j] == 0:
                img.itemset((i,j,0),r/cnt)
                img.itemset((i,j,1),g/cnt)
                img.itemset((i,j,2),b/cnt)

    return img

def remove_bg1(img):
    canny = cv.Canny(img, 100, 150)
    
    kernel = np.ones((9,9), np.uint8)
    closing = cv.morphologyEx(canny, cv.MORPH_CLOSE, kernel)
    erosion = cv.erode(closing, cv.getStructuringElement(cv.MORPH_RECT, (3,3)))
    
    v=0; cnt=0
    h, w = img.shape[:2]

    for i in range(h):
        for j in range(w):
            if erosion[i, j] == 255:
                v += img.item(i,j)
                cnt += 1

    for i in range(h):
        for j in range(w):
            if erosion[i, j] == 0:
                img.itemset((i,j),v/cnt)

    return img