import cv2 as cv
import numpy as np

def equalize_background_RGB(src, canny_threshold1=100, canny_threshold2=150, close_ksize=9, erosion_ksize=3):
    canny = cv.Canny(src, canny_threshold1, canny_threshold2)
    kernel = np.ones((close_ksize,close_ksize), np.uint8)
    closing = cv.morphologyEx(canny, cv.MORPH_CLOSE, kernel)
    erosion = cv.erode(closing, cv.getStructuringElement(cv.MORPH_RECT, (erosion_ksize,erosion_ksize)))
    mask = erosion==0
    masked = src[mask]
    eq = (np.sum(masked, axis=0)/masked.shape[0]).astype('uint8')
    mask = np.repeat(mask.reshape(tuple(list(mask.shape)+[1])), 3, axis=2)
    np.putmask(src, mask, eq)
    return src

def equalize_background_GRAY(src, canny_threshold1=100, canny_threshold2=150, close_ksize=9, erosion_ksize=3):
    src = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    canny = cv.Canny(src, canny_threshold1, canny_threshold2)
    kernel = np.ones((close_ksize,close_ksize), np.uint8)
    closing = cv.morphologyEx(canny, cv.MORPH_CLOSE, kernel)
    erosion = cv.erode(closing, cv.getStructuringElement(cv.MORPH_RECT, (erosion_ksize,erosion_ksize)))
    mask = erosion==0
    masked = src[mask]
    eq = (np.sum(masked, axis=0)/masked.shape[0]).astype('uint8')
    mask = np.repeat(mask.reshape(tuple(list(mask.shape)+[1])), 1, axis=2)
    np.putmask(src, mask, eq)
    return src

def apply(src, method, canny_threshold1, canny_threshold2, close_ksize, erosion_ksize):
    if method == 'rgb':
        return equalize_background_RGB(src, canny_threshold1, canny_threshold2, close_ksize, erosion_ksize)
    elif method == 'gray':
        return equalize_background_GRAY(src, canny_threshold1, canny_threshold2, close_ksize, erosion_ksize)
    else:
        raise KeyError('Wrong function name')