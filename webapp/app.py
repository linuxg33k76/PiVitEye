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
        mtime = os.path.getmtime(basedir + file)
        last_modified_date = datetime.datetime.fromtimestamp(mtime)
        mdate.append(last_modified_date)
    return render_template('video.html', files=files, directory=basedir, modified=mdate)


@app.route('/pcap')
def pcap():
    basedir = '/mnt/usb/pcap/'
    files = os.listdir(basedir)
    mdate = []
    for file in files:
        mtime = os.path.getmtime(basedir + file)
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


@app.route('/pcap/start/<time>', methods=['POST'])
def pcap_start(time):
    cmd = os.popen(('sh /opt/piviteye/SupportFiles/tshark.sh {0}').format(time))
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

@app.route('/speedtest/start', methods=['POST'])
def speedtest_start():
    cmd = os.popen('sudo speedtest-cli')
    msg = cmd.read()
    cmd.close()
    msg_array = msg.split('\n')
    # # Remove the last '\n' from array
    msg_array.pop()
    return render_template('output.html', msg=msg_array)

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
def system_sysuptime():
    cmd = os.popen('uptime')
    msg = cmd.read()
    cmd.close()
    msg = msg.strip('\r\n')
    return render_template('output.html', msg=msg)


@app.route('/system/restart', methods=['POST'])
def system_restart():
    cmd = os.popen('sudo shutdown -r +1')
    cmd.read()
    cmd.close()
    msg = 'User initiated Restart of System in progress...'
    return render_template('output.html', msg=msg)


@app.route('/system/shutdown', methods=['POST'])
def system_shutdown():
    cmd = os.popen('sudo shutdown -h +1')
    cmd.read()
    cmd.close()
    msg = 'User initiated Shutdown of System in progress...'
    return render_template('output.html', msg=msg)


@app.route('/video/capture/<time>', methods=['POST'])
def video_capture(time):
    cmd = os.popen(('sh /opt/piviteye/SupportFiles/webcam.sh {0}').format(time))
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


@app.route('/log/tail/<lines>', methods=['POST'])
def log_tail(lines):
    cmd = os.popen(('tail -n {0} /mnt/usb/log/piviteye.log').format(lines))
    msg = cmd.read()
    cmd.close()
    msg_array = msg.split('\n')
    # Remove the last '\n' from array
    msg_array.pop()
    return render_template('logoutput.html', msg=msg_array, lines=lines)


@app.route('/log/clear', methods=['POST'])
def log_clear():
    cmd = os.popen('sudo rm -f /mnt/usb/log/*.log')
    cmd.read()
    cmd.close()
    msg = 'User initiated DELETION of Log files is complete!'
    return render_template('output.html', msg=msg)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
