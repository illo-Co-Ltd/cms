import os
import cv2

ds_factor = 1
DEVICE_IP = os.getenv('DEVICE_IP')


class VideoCamera:
    def __init__(self):
        print('Camera initializing...')
        # capturing video
        # url설정
        url = f'rtsp://{DEVICE_IP}/stream1'
        self.video = cv2.VideoCapture(url)
        print('Camera initialized.')

    def __del__(self):
        # releasing camera
        self.video.release()

    def get_frame(self):
        # extracting frames
        ret, frame = self.video.read()
        frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor,
                           interpolation=cv2.INTER_AREA)
        return frame

class TestCamera:
    def __init__(self):
        self.video = cv2.VideoCapture()