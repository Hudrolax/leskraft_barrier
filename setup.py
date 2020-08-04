import os.path
import subprocess
from sys import platform


if __name__ == '__main__':
    if os.path.exists('requirements.txt'):
        if platform == "win32":
            subprocess.call(['pip', 'install', '-r', 'requirements.txt'])
        else:
            subprocess.call(['pip3', 'install', '-r', 'requirements.txt'])
    else:
        print('requirements.txt not found')