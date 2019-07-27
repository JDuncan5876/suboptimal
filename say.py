import subprocess

def say(text):
    cmd = "say \"{}\"".format(text)
    subprocess.call(cmd, shell=True)

if __name__ == "__main__":
    say("I'm sorry dave, I'm afraid I can't do that")
