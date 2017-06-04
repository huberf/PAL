import subprocess

useMimic = False
def speak(text):
    #os.system('mimic -t "' + text + '"')
    if useMimic:
        p = subprocess.Popen(["mimic", "-t", text], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    else:
        p = subprocess.Popen(["say", text], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
