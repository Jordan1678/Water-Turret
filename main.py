import cv2
import RPi.GPIO as GPIO

from TurretMode import set_mode, get_mode
from flask import Flask, render_template, Response, request

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)


camera = cv2.VideoCapture(0)
app = Flask(__name__)

set_mode("Off")

Base = 12
Arm = 13
ValveOPEN = 23
ValveCLOSE = 24

GPIO.setup(ValveOPEN, GPIO.OUT)
GPIO.setup(ValveCLOSE, GPIO.OUT)

BasePWM = GPIO.PWM(Base, 50)
ArmPWM = GPIO.PWM(Arm, 50)
BasePWM.start(0)
ArmPWM.start(0)

GPIO.output(ValveOPEN, GPIO.LOW)
GPIO.output(ValveCLOSE, GPIO.LOW)


def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def AimTurret(x, y):
    xTarget = map(x/ 2, 0, 640, 90 + 45, 90 - 45)
    yTarget = map(y/ 2, 0, 480, 90 - 32, 90 + 32)

    BasePWM.ChangeDutyCycle(xTarget/ 18 + 2)
    ArmPWM.ChangeDutyCycle(yTarget / 18 + 2)
    print(f"Face Found @ {xTarget}x {yTarget}y")
    pass


def StartTurret():
    GPIO.output(ValveOPEN, GPIO.HIGH)
    GPIO.output(ValveCLOSE, GPIO.LOW)
    pass


def StopTurret():
    GPIO.output(ValveOPEN, GPIO.LOW)
    GPIO.output(ValveCLOSE, GPIO.HIGH)
    pass


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/TurretMode', methods=['GET', 'POST'])
def TurretMode():

    if request.method == 'GET':
        print("TurretMode: ", get_mode())
        return get_mode()

    if request.method == 'POST':
        # if the post request returns Manual, then run the Manual mode
        if request.form['TurretMode'] == 'Off':
            set_mode("Off")
            print('Turret Mode: Off')
            return 'Turret Mode: Off'

        # if the post request returns Manual, then run the Manual mode
        if request.form['TurretMode'] == 'Manual':
            try:
                xPOS = int(request.form['x'])
                yPOS = int(request.form['y'])
                AimTurret(xPOS, yPOS)
            except:
                set_mode("Manual")
                print('Turret Mode: Manual')
                return 'Turret Mode: Manual'

        # if the post request returns Auto, then run the auto mode
        if request.form['TurretMode'] == 'Auto':
            set_mode("Auto")
            print('Turret Mode: Auto')
            return 'Turret Mode: Auto'

        # if the post request returns Start, then run the start mode
        if request.form['TurretMode'] == 'Start':
            StartTurret()
            print('Turret Mode: Start')
            return 'Turret Mode: Start'

        # if the post request returns Stop, then run the stop mode
        if request.form['TurretMode'] == 'Stop':
            StopTurret()
            print('Turret Mode: Stop')
            return 'Turret Mode: Stop'


# A function to generate the frames from the camera and make them a video
def gen():
    # get camera
    cap = cv2.VideoCapture(0)

    cap.set(3, 640)  # vertical cap
    cap.set(4, 480)  # horizontal cap

    # Read until frame is completed
    while (cap.isOpened()):

        # Capture frame-by-frame
        ret, img = cap.read()
        if get_mode() == "Auto":
            face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            face = face_cascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=4)
        
            for (x, y, w, h) in face:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 5)
                cv2.putText(img, "Face", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                AimTurret(x + w/2, y + h/2)

            if ret:
                img = cv2.resize(img, (0, 0), fx=1, fy=1)

                frame = cv2.imencode('.jpg', img)[1].tobytes()
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            else:
                break

        else:
            if ret:
                img = cv2.resize(img, (0, 0), fx=1, fy=1)

                frame = cv2.imencode('.jpg', img)[1].tobytes()
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            else:
                break

# responds with the generated frames
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


app.run(host='0.0.0.0', port=80)
