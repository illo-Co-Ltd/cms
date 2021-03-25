import cv2


def average(src, ksize):
    return cv2.blur(src, ksize=(ksize, ksize))


def median(src, ksize):
    return cv2.medianBlur(src, ksize=ksize)


def gaussian(src, ksize):
    return cv2.GaussianBlur(src=src, ksize=(ksize, ksize))


def apply(src, method, ksize):
    if method == 'average':
        return average(src, ksize)
    elif method == 'median':
        return median(src, ksize)
    elif method == 'gaussian':
        return gaussian(src, ksize)
    else:
        raise KeyError('Wrong function name')

