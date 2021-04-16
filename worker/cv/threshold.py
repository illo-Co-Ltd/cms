import cv2

TYPEMAP = {
    'binary': cv2.THRESH_BINARY,
    'binary_inv': cv2.THRESH_BINARY_INV,
    'trunc': cv2.THRESH_TRUNC,
    'tozero': cv2.THRESH_TOZERO,
    'tozero_inv': cv2.THRESH_TOZERO_INV,
}


def threshold(src, mode, thresh_type, thresh, maxval):
    if mode == 'simple':
        return cv2.threshold(src, thresh, maxval, TYPEMAP[thresh_type])
    elif mode == 'otsu':
        return cv2.threshold(src, 0, maxval, TYPEMAP[thresh_type] + cv2.THRESH_OTSU)
    else:
        raise KeyError('Wrong function name')


def adaptive_threshold(src, mode, thresh_type, maxval, bsize, c):
    if mode == 'mean':
        return cv2.adaptiveThreshold(src, maxval, cv2.ADAPTIVE_THRESH_MEAN_C, TYPEMAP[thresh_type], bsize, c)
    elif mode == 'gaussian':
        return cv2.adaptiveThreshold(src, maxval, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, TYPEMAP[thresh_type], bsize, c)
    else:
        raise KeyError('Wrong function name')


def apply(src, method, mode, thresh_type, *args, **kwargs):
    if method == 'global':
        return threshold(src, mode, thresh_type, *args, **kwargs)
    elif method == 'adaptive':
        return adaptive_threshold(src, mode, thresh_type, *args, **kwargs)
    else:
        raise KeyError('Wrong function name')
