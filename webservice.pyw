import time
import sys
import signal
import logging
import os
import ctypes
import ctypes.wintypes
import threading
import SimpleHTTPServer
import SocketServer
import posixpath
import urllib

path = os.path.dirname(__file__)
service_name = os.path.splitext(os.path.basename(__file__))[0]
fname= os.path.splitext(__file__)[0]+".log"

logging.basicConfig(filename=fname,
                    level=logging.DEBUG)

class h1(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = self.base_path
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        return path
    def address_string(self):
        host, port = self.client_address[:2]
        return (host, port)
    pass



def install_service():
    global service_name
    import os
    fname=os.path.basename(__file__)
    
    print fname
    command = "sc create %s binPath= \"\\\"C:\\Python27\\pythonw.exe\\\" \\\"C:\\Documents and Settings\\User\\Desktop\\javad\\servers\\windiws service\\%s\\\"\" start= auto"%(service_name,fname)
    print command
    print os.system(command)
def uninstall_service():
    global service_name
    import os
    fname=os.path.basename(__file__)

    
    print fname
    command = "sc delete %s "%(service_name)
    print command
    print os.system(command)

SERVICE_MAIN_FUNCTION = ctypes.WINFUNCTYPE(None, ctypes.wintypes.DWORD, ctypes.wintypes.LPCSTR)
class _SERVICE_TABLE_ENTRY(ctypes.Structure):
    _fields_=[
        ("lpServiceName",ctypes.POINTER(ctypes.c_wchar_p)),
        ("lpServiceProc",SERVICE_MAIN_FUNCTION),
              ]
SERVICE_CTL_FUNCTION = ctypes.WINFUNCTYPE(None,ctypes.wintypes.DWORD)
def ServiceCtrlHandler(CtrlCode):
    global service_name,path
    logging.info('55')
    logging.info(str(CtrlCode))
    while True:
        time.sleep(1)
class _SERVICE_STATUS (ctypes.Structure):
    _fields_=[
        ("dwServiceType",ctypes.wintypes.DWORD),
        ("dwCurrentState",ctypes.wintypes.DWORD),
        ("dwControlsAccepted",ctypes.wintypes.DWORD),
        ("dwWin32ExitCode",ctypes.wintypes.DWORD),
        ("dwServiceSpecificExitCode",ctypes.wintypes.DWORD),
        ("dwCheckPoint",ctypes.wintypes.DWORD),
        ("dwWaitHint",ctypes.wintypes.DWORD),

              ]
def service_job():
    global path
    logging.info('start job')
    try:
        PORT = 80
        h1.base_path=os.path.join(path,"root")
        server= SocketServer.ThreadingTCPServer(("", PORT), h1)
        logging.info('server start on port %d '%PORT)
        server.serve_forever()
    except Exception,e:
        logging.exception('eeee4')
        logging.exception(str(e))
    logging.info('stop job')

def handle_term(signum, frame):
    pass
    logging.info('7')
    try:
        sss=ctypes.windll.advapi32.SetServiceStatus
        gst=_SERVICE_STATUS()
        gst.dwCurrentState=ctypes.wintypes.DWORD(0x00000001) #SERVICE_STOPPED
        gst.dwControlsAccepted=ctypes.wintypes.DWORD(0x00000000)  
        gst.dwWin32ExitCode=ctypes.wintypes.DWORD(0)
##        gst.dwServiceSpecificExitCode=ctypes.wintypes.DWORD(0)
        gst.dwCheckPoint=ctypes.wintypes.DWORD(3)
##        gst.dwWaitHint=ctypes.wintypes.DWORD(0)
        logging.info('71')
        res=sss(sh,ctypes.pointer(gst))
        logging.info(str(res))
    except Exception,e:
        logging.exception('eeee7')
        logging.exception(str(e))
def run_job():
    t=threading.Thread(target=service_job)
    t.daemon=True
    t.start()
    t.join()
    
def service_main(argc,argv):
    global service_name
    logging.info('3')
    try:
        rh=ctypes.windll.advapi32.RegisterServiceCtrlHandlerW
        sss=ctypes.windll.advapi32.SetServiceStatus
        getLastError=ctypes.windll.kernel32.GetLastError
        cevn=ctypes.windll.kernel32.CreateEventW
        sh=rh(ctypes.pointer(ctypes.c_wchar_p(service_name) ),SERVICE_CTL_FUNCTION(ServiceCtrlHandler))
        logging.info(str(sh))
        if sh==0:
            err=getLastError()
            logging.error(str(err))
            return 
        logging.info('31')
        gst=_SERVICE_STATUS()
        gst.dwServiceType=ctypes.wintypes.DWORD(0x00000010) #SERVICE_WIN32_OWN_PROCESS
        gst.dwCurrentState=ctypes.wintypes.DWORD(0x00000002) #SERVICE_START_PENDING
        gst.dwControlsAccepted=ctypes.wintypes.DWORD(0)
        gst.dwWin32ExitCode=ctypes.wintypes.DWORD(0)
        gst.dwServiceSpecificExitCode=ctypes.wintypes.DWORD(0)
        gst.dwCheckPoint=ctypes.wintypes.DWORD(0)
        gst.dwWaitHint=ctypes.wintypes.DWORD(0)
        res=sss(sh,ctypes.pointer(gst))
        logging.info(str(res))
        if res==0:
            err=getLastError()
            logging.error(str(err))
            return 
        logging.info('32')
        evn_stop=cevn(None,ctypes.c_bool(True),ctypes.c_bool(False),None)
        logging.info('321')
        logging.info(str(evn_stop))
        if evn_stop==0:
##            gst=_SERVICE_STATUS()
##            gst.dwServiceType=ctypes.wintypes.DWORD(0)
            gst.dwCurrentState=ctypes.wintypes.DWORD(0x00000004) #SERVICE_STOPPED
            gst.dwControlsAccepted=ctypes.wintypes.DWORD(0)
            gst.dwWin32ExitCode=getLastError()
##            gst.dwServiceSpecificExitCode=ctypes.wintypes.DWORD(0)
            gst.dwCheckPoint=ctypes.wintypes.DWORD(1)
##            gst.dwWaitHint=ctypes.wintypes.DWORD(0)
            logging.info(str(sh))

            logging.info('322')
            res=sss(sh,ctypes.pointer(gst))

                
            logging.info('33')
            if res==0:
                err=getLastError()
                logging.error(str(err))
            return 
            
##        gst=_SERVICE_STATUS()
##        gst.dwServiceType=ctypes.wintypes.DWORD(0)
        gst.dwCurrentState=ctypes.wintypes.DWORD(0x00000004) #SERVICE_RUNNING
        gst.dwControlsAccepted=ctypes.wintypes.DWORD(0x00000001)  #SERVICE_ACCEPT_STOP
        gst.dwWin32ExitCode=ctypes.wintypes.DWORD(0)
##        gst.dwServiceSpecificExitCode=ctypes.wintypes.DWORD(0)
        gst.dwCheckPoint=ctypes.wintypes.DWORD(0)
##        gst.dwWaitHint=ctypes.wintypes.DWORD(0)
        logging.info('4')
        res=sss(sh,ctypes.pointer(gst))
        logging.info(str(res))
        if res==0:
            err=getLastError()
            logging.error(str(err))
            return
    except Exception,e:
        logging.exception('eeee1')
        logging.exception(str(e))
    run_job()
    logging.info('sss4')
    try:
        gst.dwCurrentState=ctypes.wintypes.DWORD(0x00000001) #SERVICE_STOPPED
        gst.dwControlsAccepted=ctypes.wintypes.DWORD(0x00000000)  
        gst.dwWin32ExitCode=ctypes.wintypes.DWORD(0)
##        gst.dwServiceSpecificExitCode=ctypes.wintypes.DWORD(0)
        gst.dwCheckPoint=ctypes.wintypes.DWORD(3)
##        gst.dwWaitHint=ctypes.wintypes.DWORD(0)
        logging.info('6')
        res=sss(sh,ctypes.pointer(gst))
        logging.info(str(res))
    except Exception,e:
        logging.exception('eeee2')
        logging.exception(str(e))
def main():
    global service_name
    logging.info('2')
    sd=ctypes.windll.advapi32.StartServiceCtrlDispatcherW
    getLastError=ctypes.windll.kernel32.GetLastError
    try:
        signal.signal(signal.SIGINT, handle_term)
        signal.signal(signal.SIGTERM, handle_term)
        
##        ServiceTable=_SERVICE_TABLE_ENTRY()
        lpServiceTable=(_SERVICE_TABLE_ENTRY*2)()
        
        lpServiceTable[0].lpServiceName=ctypes.pointer(ctypes.c_wchar_p(service_name) )
        lpServiceTable[0].lpServiceProc=SERVICE_MAIN_FUNCTION(service_main)
##        lpServiceTable[0]=ServiceTable
##        logging.info(str(sd))
        res=sd(lpServiceTable)
        logging.info(str(res))
        if res==0:
            err=getLastError()
            logging.error(str(err))
##        logging.info(str(lpServiceTable))
##        logging.info(str(dir(lpServiceTable)))
##        logging.info(lpServiceTable.contents)
        
        logging.info(str(dir(lpServiceTable[0].lpServiceName)))
        logging.info(lpServiceTable[0].lpServiceName)
    except Exception,e:
        logging.exception('1')
        logging.exception(str(e))
##    try:
##        while True:
##            time.sleep(1)
##    except Exception,e:
##        logging.exception('eeee3')
##        logging.exception(str(e))
if __name__=="__main__":
    print len(sys.argv)
    if len(sys.argv)==2:
        if sys.argv[1]=='install':
            install_service()
        if sys.argv[1]=='uninstall':
            uninstall_service()
        if sys.argv[1]=='test':
            run_job()
    else:
        main()
##    while True:
##        time.sleep(1)
