import sh
from sh import git
import time
import os, sys
import psutil
import logging

aggregated = ""

def CheckForUpdate(workingDir):
    print("Fetching most recent code from source..." + workingDir)

    # Fetch most up to date version of code.
    p = git("--git-dir=" + workingDir + ".git/", "--work-tree=" + workingDir, "fetch", "origin", "master", _out=ProcessFetch, _out_bufsize=0, _tty_in=True)               
    
    print("Fetch complete.")
    time.sleep(2)
    print("Checking status for " + workingDir + "...")
    statusCheck = git("--git-dir=" + workingDir + ".git/", "--work-tree=" + workingDir, "status")

    if "Your branch is up-to-date" in statusCheck:
        print("Status check passes.")
        print("Code up to date.")
        return False
    else:
        print("Code update available.")
        return True

def ProcessFetch(char, stdin):
    global aggregated

    sys.stdout.flush()
    aggregated += char
    if aggregated.endswith("Password for 'https://yourrepo@bitbucket.org':"):
        print(mainLogger, "Entering password...", True)
        stdin.put("yourpassword\n")

def restart_program():
    """Restarts the current program, with file objects and descriptors
       cleanup
    """

    try:
        p = psutil.Process(os.getpid())
        for handler in p.get_open_files() + p.connections():
            os.close(handler.fd)
    except Exception as e:
        logging.error(e)

    python = sys.executable
    os.execl(python, python, *sys.argv)

if __name__ == "__main__":
    checkTimeSec = 60
    gitDir = os.getcwd() + '/'

    while True:
        print("*********** Checking for code update **************")                                                     
    
        if CheckForUpdate(gitDir):
            pulled = git('pull', 'origin', 'master')
            print(pulled[0])

            print("Resetting code...")
            print(sys.executable)
            os.execl(sys.executable, sys.executable, *sys.argv)

        print("Check complete. Waiting for " + str(checkTimeSec) + "seconds until next check...", True)
        time.sleep(checkTimeSec)

