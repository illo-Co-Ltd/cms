import cv2


def average_blur(src, ksize, anchor):
    res = cv2.blur(src, ksize=(ksize, ksize), )
    return res


def median_blur(src, ksize):
    res = cv2.blur(src, ksize=(ksize, ksize))
    return res


def gaussian_blur(src, ksize):
    res = cv2.GaussianBlur(src=src, ksize=ksize)
    return res