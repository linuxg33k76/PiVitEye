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
    cmd = os.popen('sh /opt/piviteye/SupportFiles/tshark.sh')
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


@app.route('/system/update', methods=['POST'])
def system_update():
    cmd = os.popen('sudo apt-get update && sudo apt-get upgrade -y')
    cmd.read()
    cmd.close()
    msg = 'User initiated Update of System is complete!'
    return render_template('output.html', msg=msg)


@app.route('/system/uptime', methods=['POST'])
def system_uptime():
    cmd = os.popen('sudo service motion stop')
    msg = cmd.read()
    cmd.close()
    return render_template('output.html', msg=msg)


@app.route('/system/restart', methods=['POST'])
def system_restart():
    cmd = os.popen('sudo shutdown -r now')
    cmd.read()
    cmd.close()
    msg = 'User initiated Restart of System in progress...'
    return render_template('output.html', msg=msg)


@app.route('/system/shutdown', methods=['POST'])
def system_shutdown():
    cmd = os.popen('sudo shutdown -h now')
    cmd.read()
    cmd.close()
    msg = 'User initiated Shutdown of System in progress...'
    return render_template('output.html', msg=msg)


@app.route('/video/capture', methods=['POST'])
def video_capture():
    cmd = os.popen('sh /opt/piviteye/SupportFiles/webcam.sh')
    cmd.read()
    cmd.close()
    msg = 'User initiated video capture is complete!'
    return render_template('output.html', msg=msg)


@app.route('/video/clear', methods=['POST'])
def video_clear():
    cmd = os.popen('sudo rm -f /mnt/usb/video/*.*')
    cmd.read()
    cmd.close()
    msg = 'User initiated DELETION of Video files is complete!'
    return render_template('output.html', msg=msg)


@app.route('/log/tail', methods=['POST'])
def log_tail():
    cmd = os.popen('tail -n 30 /mnt/usb/log/piviteye.log')
    msg = cmd.read()
    cmd.close()
    msg_array = msg.split('\n')
    # Remove the last '\n' from array
    msg_array.pop()
    return render_template('logoutput.html', msg=msg_array)


@app.route('/log/clear', methods=['POST'])
def log_clear():
    cmd = os.popen('sudo rm -f /mnt/usb/log/*.log')
    cmd.read()
    cmd.close()
    msg = 'User initiated DELETION of Log files is complete!'
    return render_template('output.html', msg=msg)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
