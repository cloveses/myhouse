import os
import time
import signal
import subprocess
from flask import (Flask ,request, url_for, abort, redirect, g,
                    make_response, session, render_template, render_template_string)

signal.signal(signal.SIGCHLD, signal.SIG_IGN)

app = Flask(__name__)

@app.route('/')
def index():
    p = subprocess.Popen(['python3', '/home/djx/mytest/sub.py'])
    print(p.pid)
    return "<h1>Hello Flask</h1>"

@app.route('/aa/<int:pid>')
def indexa(pid):
    os.kill(pid, signal.SIGTSTP)
    return "<h1>Hello 2 Flask</h1>"