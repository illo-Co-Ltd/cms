import cv2


def canny(src, th1, th2, asize, L2):
    return cv2.Canny(src, threshold1=th1, threshold2=th2, apertureSize=asize, L2gradient=L2)


def circle(src):
    pass


def line(src):
    pass


def apply(src, method, **kwargs):
    if method == 'canny':
        return canny(src, **kwargs)
    if method == 'circle':
        return circle(src, **kwargs)
    if method == 'line':
        return line(src, **kwargs)
    else:
        raise KeyError('Wrong function name')
