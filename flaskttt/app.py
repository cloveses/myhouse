import os
import time
import signal
import subprocess
from flask import (Flask ,request, url_for, abort, redirect, jsonify,
                    make_response, session, render_template, render_template_string)
from waitress import serve


app = Flask(__name__)


def save_pid(pid):
    with open('pid.dat', 'w') as f:
        f.write(str(pid))

def get_pid(clear=True):
    if not os.path.exists('pid.dat'):
        return 0
    with open('pid.dat', 'r') as f:
        try:
            pid = int(f.readline().strip())
        except:
            pid = 0
    if clear:
        save_pid('\n')
    return pid

@app.route('/', methods=["GET","POST"])
def index():
    info = ''
    if request.method == "GET":
        return render_template('login.html', info=info)
    else:
        name = request.form.get('name', '')
        password = request.form.get('password', '')
        if name and password and name == 'lenovo' and password == 'lenovolen':
            pid = get_pid(clear=False)
            return render_template('index.html', pid=pid)
        else:
            info = 'LOG ERROR!'
            return render_template('login.html',info=info)

@app.route('/start')
def start():
    try:
        p = subprocess.Popen(['python3', '/home/djx/mytest/sub.py'])
        print(p.pid)
        save_pid(p.pid)
        pass
    except:
        return jsonify(status=1)
    else:
        return jsonify(status=0, pid=p.pid)
    # return jsonify(status=0,pid=15)

@app.route('/end/<int:pid>')
def end(pid):
    pid = get_pid()
    if pid:
        os.kill(pid, signal.SIGTSTP)
        return jsonify(status=0)
    else:
        return jsonify(status=1)

if __name__ == '__main__':
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    serve(app, listen='119.23.106.87:5000')