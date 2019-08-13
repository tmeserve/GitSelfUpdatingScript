import sh
from sh import git
import time
import os, sys
import logging

aggregated = ""

def CheckForUpdate(workingDir):
    print("Fetching most recent code from source..." + workingDir)

    p = git("--git-dir=" + workingDir + ".git/", "--work-tree=" + workingDir, "fetch", "origin", "master", _out=ProcessFetch, _out_bufsize=0, _tty_in=True)

    print("Fetch complete.")
    time.sleep(2)
    print("Checking status for " + workingDir + "...")
    statusCheck = git('fetch', '--dry-run', '--all')

    
    if 'remote:' in statusCheck:
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
        checked = CheckForUpdated(getDir)
        print(checked, ' is checked'
        if CheckForUpdate(gitDir):
            pulled = git('pull', 'origin', 'master')
            print(pulled)
            print("Restarting Program...")
            os.execl(sys.executable, sys.executable, *sys.argv)

        print("Check complete. Waiting for " + str(checkTimeSec) + "seconds until next check...", True)
        time.sleep(checkTimeSec)

