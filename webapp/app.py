# app.py
# Created by Ben Calvert on 10/17/16.

from flask import Flask, render_template
import os


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/log')
def log():
    basedir = '/mnt/usb/log/'
    files = os.listdir(basedir)

    return render_template('log.html', files=files, directory=basedir)


@app.route('/videos')
def video():
    basedir = '/mnt/usb/video/'
    files = os.listdir(basedir)
    return render_template('video.html', files=files, directory=basedir)


@app.route('/pcap')
def pcap():
    basedir = '/mnt/usb/pcap/'
    files = os.listdir(basedir)
    return render_template('pcap.html', files=files, directory=basedir)


@app.route('/stream')
def stream():
    cmd = os.popen('sudo service motion status')
    msg = cmd.read()
    cmd.close()
    if 'inactive (dead)' in msg:
        return render_template('nolivefeed.html')
    else:
        return render_template('livefeed.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
