import os
import time
import signal
import subprocess
from flask import (Flask ,request, url_for, abort, redirect, jsonify,
                    make_response, session, render_template, render_template_string)
# from waitress import serve


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start')
def start():
    # try:
        # p = subprocess.Popen(['python3', '/home/djx/mytest/sub.py'])
        # print(p.pid)
    #     pass
    # except:
    #     return jsonify(status=1)
    # else:
    #     return jsonify(status=0, pid=p.pid)
    return jsonify(status=0,pid=15)

@app.route('/end/<int:pid>')
def end(pid):
    # os.kill(pid, signal.SIGTSTP)
    return jsonify(status=0)

# if __name__ == '__main__':
#     signal.signal(signal.SIGCHLD, signal.SIG_IGN)
#     serve(app, listen='*:5000')