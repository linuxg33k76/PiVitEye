# app.py
# Created by Ben Calvert on 10/17/16.

from flask import Flask, render_template
import os
import datetime


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/log')
def log():
    basedir = '/mnt/usb/log/'
    files = os.listdir(basedir)
    mdate = []
    for file in files:
        mtime = os.path.getmtime(basedir+file)
        last_modified_date = datetime.datetime.fromtimestamp(mtime)
        mdate.append(last_modified_date)

    return render_template('log.html', files=files, directory=basedir, modified=mdate)


@app.route('/videos')
def video():
    basedir = '/mnt/usb/video/'
    files = os.listdir(basedir)
    mdate = []
    for file in files:
        mtime = os.path.getmtime(basedir+file)
        last_modified_date = datetime.datetime.fromtimestamp(mtime)
        mdate.append(last_modified_date)
    return render_template('video.html', files=files, directory=basedir, modified=mdate)


@app.route('/pcap')
def pcap():
    basedir = '/mnt/usb/pcap/'
    files = os.listdir(basedir)
    mdate = []
    for file in files:
        mtime = os.path.getmtime(basedir+file)
        last_modified_date = datetime.datetime.fromtimestamp(mtime)
        mdate.append(last_modified_date)
    return render_template('pcap.html', files=files, directory=basedir, modified=mdate)


@app.route('/stream')
def stream():
    cmd = os.popen('sudo service motion status')
    msg = cmd.read()
    cmd.close()
    if 'inactive (dead)' in msg:
        return render_template('nolivefeed.html')
    else:
        return render_template('livefeed.html')

@app.route('/pcap/start', methods=['POST'])
def pcap_start():
    cmd = os.popen('sudo tshark -i eth0 -a duration:30 -b filesize:2048 -w /mnt/usb/pcap/output.pcap -F pcap')
    cmd.read()
    cmd.close()
    msg = 'User initiated packet capture is complete!'
    return render_template('output.html', msg=msg)

@app.route('/pcap/clear', methods=['POST'])
def pcap_clear():
    cmd = os.popen('sudo rm -f /mnt/usb/pcap/*.pcap')
    cmd.read()
    cmd.close()
    msg = 'User initiated DELETION of PCAP files is complete!'
    return render_template('output.html', msg=msg)

@app.route('/motion/start', methods=['POST'])
def motion_start():
    cmd = os.popen('sudo service motion start')
    cmd.read()
    cmd.close()
    msg = 'User initiated Start of Motion Service files is complete!'
    return render_template('output.html', msg=msg)

@app.route('/motion/stop', methods=['POST'])
def motion_stop():
    cmd = os.popen('sudo service motion stop')
    cmd.read()
    cmd.close()
    msg = 'User initiated Stop of Motion Service is complete!'
    return render_template('output.html', msg=msg)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
