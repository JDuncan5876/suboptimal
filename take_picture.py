import subprocess
import random

def take_picture():
    n = random.randint(0, 100000) 
    path = "/tmp/" + str(n) + ".jpg"
    cmd = "raspistill -o " + path
    print(cmd)
    subprocess.call(cmd, shell=True)
    return path

if __name__ == "__main__":
    take_picture()
