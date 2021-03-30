import cv2


def canny(src, th1, th2, asize, L2):
    return cv2.Canny(src, threshold1=th1, threshold2=th2, apertureSize=asize, L2gradient=L2)


def circle(src, dp, minDist, param1, param2, minRadius, maxRadius, alt=False):
    if not alt:
        return cv2.HoughCircles(src, cv2.HOUGH_GRADIENT, dp=dp, minDist=minDist, param1=param1, param2=param2,
                                minRadius=minRadius, maxRadius=maxRadius)
    else:
        return cv2.HoughCircles(src, cv2.HOUGH_GRADIENT_ALT, dp=dp, minDist=minDist, param1=param1, param2=param2,
                                minRadius=minRadius, maxRadius=maxRadius)


def line(src, rho, theta, threshold):
    return cv2.HoughLines(src, rho=rho, theta=theta, threshold=threshold)


def apply(src, method, *args, **kwargs):
    if method == 'canny':
        return canny(src, *args, **kwargs)
    if method == 'circle':
        return circle(src, *args, **kwargs)
    if method == 'line':
        return line(src, *args, **kwargs)
    else:
        raise KeyError('Wrong function name')
