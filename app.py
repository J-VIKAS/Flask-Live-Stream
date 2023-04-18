from flask import Flask, render_template, Response, redirect
import cv2

app=Flask(__name__)

def generate_frames():

    while True:
        camera.set(3,1920);
        camera.set(4,1920);
        success,frame=camera.read()
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start')
def start():
    global camera
    print("Starting Camera")
    camera = cv2.VideoCapture(0)
    print("Started Camera")
    return render_template('start.html')

@app.route('/stop')
def stop():
    camera.release()
    cv2.destroyAllWindows()
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)

