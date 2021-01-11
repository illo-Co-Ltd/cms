import cv2

ds_factor = 0.8


class VideoCamera(object):
    def __init__(self):
        print('Camera initializing...')
        # capturing video
        # url설정
        url = 'rtsp://192.168.50.39/stream1'
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
        """
        # face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in face_rects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            break
        """
        # encode OpenCV raw frame to jpg and displaying it
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
