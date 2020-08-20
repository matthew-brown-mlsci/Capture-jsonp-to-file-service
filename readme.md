## Capture JSONP request to file (Python Windows Service)

Windows service that runs a flask server that accepts JSONP GET requests, capturing 
data as GET request parameters.  As part of a migration project, I needed to collect some
data from an application.  I injected an ajax jsonp call into a medical forms web 
app in question, and then setup this python service on an internal server to log
the jsonp requests to a file.  

Tested on MS Server 2012 \w WinPython 3.7.1

Compiling to service + install (in winpython cmd as admin):
```
    set PYTHONHOME=C:\python37\python-3.7.1.amd64\
    set PYTHONPATH=C:\python37\python-3.7.1.amd64\Lib\
    pip install pyinstaller
    pyinstaller -F --hidden-import=win32timezone "capture_jsonp_to_file_service.py"
    "dist\capture_jsonp_to_file_service.exe install"
    sc start "Capture JSONP to file service"
```

Testing (using curl):
```
    curl -s "http://localhost:9123/?data=HelloWorld"
```

Or via javascript jquery ajax request:
```
$.ajax({
    url: "http://localhost:9123/",
    data: { data: "HelloWorld" },
    dataType: "jsonp"
});
```