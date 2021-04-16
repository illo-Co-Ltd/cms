import cv2


def global_he(src):
    return cv2.equalizeHist(src)


def clahe(src, clipLimit, tileGridSize):
    instance = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=tileGridSize)
    dst = instance.apply(src)
    del instance
    return dst


def apply(src, method, *args, **kwargs):
    if method == 'global':
        return global_he(src, *args, **kwargs)
    elif method == 'clahe':
        return clahe(src, *args, **kwargs)
    else:
        raise KeyError('Wrong function name')
