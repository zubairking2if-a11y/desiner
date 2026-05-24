from flask import Flask, Response
import mss
import cv2
import numpy as np

app = Flask(__name__)

def generate_screen():
    with mss.mss() as sct:

        monitor = sct.monitors[1]

        while True:
            screenshot = sct.grab(monitor)

            frame = np.array(screenshot)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            _, buffer = cv2.imencode(
                '.jpg',
                frame,
                [cv2.IMWRITE_JPEG_QUALITY, 60]
            )

            frame_bytes = buffer.tobytes()

            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' +
                frame_bytes +
                b'\r\n'
            )

@app.route('/')
def index():
    return """
    <html>
    <head>
        <title>Screen Share</title>
    </head>
    <body style="margin:0;background:black;">
        <img src="/video" width="100%">
    </body>
    </html>
    """

@app.route('/video')
def video():
    return Response(
        generate_screen(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
