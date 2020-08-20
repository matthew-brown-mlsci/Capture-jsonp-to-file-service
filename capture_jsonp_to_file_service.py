"""

    Windows service that runs a flask server that accepts JSONP GET requests, capturing 
    data as GET request parameters.  As part of a migration project, I needed to collect some
    data from an application.  I injected an ajax jsonp call into a medical forms web 
    app in question, and then setup this python service on an internal server to log
    the jsonp requests to a file.  

    Tested on MS Server 2012 \w WinPython 3.7.1

    Compiling to service + install (in winpython cmd as admin):
        set PYTHONHOME=C:\python37\python-3.7.1.amd64\
	    set PYTHONPATH=C:\python37\python-3.7.1.amd64\Lib\
        pip install pyinstaller
        pyinstaller -F --hidden-import=win32timezone "capture_jsonp_to_file_service.py"
        "dist\capture_jsonp_to_file_service.exe install"
        sc start "Capture JSONP to file service"


    Testing (using curl):
        curl -s "http://localhost:9123/?data=HelloWorld"

    Or via javascript jquery ajax request:

    $.ajax({
        url: "http://localhost:9123/",
        data: { data: "HelloWorld" },
        dataType: "jsonp"
    });

"""

import servicemanager
import socket
import sys
import win32event
import win32service
import win32serviceutil
import datetime

from myapp import app

logfile = "C:\\scripts\\Capture-jsonp-to-file-service\\Capture-jsonp-to-file-service-log.txt"
port = 9123

#Make logging a little easier
def log_entry(log_message):
	with open(logfile, 'a') as f:
		f.write(str(datetime.datetime.now()) + " : ")
		f.write(log_message + '\n')

class CaptureService(win32serviceutil.ServiceFramework):
    _svc_name_ = "Capture JSONP to file service"
    _svc_display_name_ = "Capture JSONP to file service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(10)

    def SvcStop(self):
        log_entry('SvcStop started')
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        log_entry('SvrStop finished')

    def SvcDoRun(self):
        log_entry('SvrDoRun started')
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        self.flaskmain()
        
    def flaskmain(self):
        log_entry('flaskmain() started')
        app.run(debug=False, host='0.0.0.0', port=port)
        log_entry('flaskmain() finished')


if __name__ == '__main__':
    log_entry("Capture JSONP to file service started")
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(CaptureService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(CaptureService)
    log_entry("Capture JSONP to file service stopped")