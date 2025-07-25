from flask import Flask, render_template, Response, redirect, url_for
from jump_detector import gen_frames, jump_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', data=None)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop')
def stop():
    # After pressing Stop, show results
    return render_template('index.html', data=jump_data["all_jumps"])

if __name__ == '__main__':
    app.run(debug=True)
