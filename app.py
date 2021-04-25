from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
import platform,socket,re,uuid,json,psutil,logging
import os, sys, glob, re
import geocoder
import subprocess

app = Flask(__name__)


def getSystemInfo():
    try:
        Id = subprocess.check_output(['systeminfo']).decode('utf-8').split('\n')
        new = []
        
        # arrange the string into clear info
        for item in Id:
        	new.append(str(item.split("\r")[:-1]))
        info={}
        info['platform']=platform.system()
        info['platform-release']=platform.release()
        info['platform-version']=platform.version()
        info['architecture']=platform.machine()
        info['hostname']=socket.gethostname()
        info['ip-address']=socket.gethostbyname(socket.gethostname())
        info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor']=platform.processor()
        info['ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        info["location"]=str(geocoder.ip('me'))
        info['More'] = new
        return json.dumps(info)
    except Exception as e:
        logging.exception(e)
    

@app.route('/',methods=['GET'])
def index():
    #return render_template('index.html')
    info = getSystemInfo()
    return info


if __name__ == '__main__':
    app.run(debug=True,threaded=False)
