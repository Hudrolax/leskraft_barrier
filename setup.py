import os.path
import subprocess

if __name__ == '__main__':
    if os.path.exists('requirements.txt'):
        subprocess.call(['pip', 'install', '-r requirements.txt'])
    else:
        print('requirements.txt not found')