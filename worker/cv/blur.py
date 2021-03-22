import cv2


def average_blur(src, ksize, anchor):
    res = cv2.blur(src, ksize=(ksize, ksize), )


def median_blur(src, ksize):
    res = cv2.blur(src, ksize=(ksize, ksize), )


def gaussian_blur(img):
    pass