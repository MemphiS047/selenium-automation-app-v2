import os
import subprocess
import tarfile
import zipfile
from urllib.request import urlopen

from bs4 import BeautifulSoup


def get_firefox_version(platform):
    """
    :return: the version of firefox installed on client
    """
    if platform == 'linux':
        with subprocess.Popen(['firefox', '--version'], stdout=subprocess.PIPE) as proc:
            version = proc.stdout.read().decode('utf-8').replace('Mozilla Firefox', '').strip()
    elif platform == 'mac':
        process = subprocess.Popen(['/Applications/Firefox.app/Contents/MacOS/firefox', '--version'], stdout=subprocess.PIPE)
        version = process.communicate()[0].decode('UTF-8').replace('Mozilla Firefox', '').strip()
    elif platform == 'win32':
        path1 = 'C:\\PROGRA~1\\Mozilla Firefox\\firefox.exe'
        path2 = 'C:\\PROGRA~2\\Mozilla Firefox\\firefox.exe'
        if os.path.exists(path1):
            process = subprocess.Popen([path1, '-v', '|', 'more'], stdout=subprocess.PIPE)
        elif os.path.exists(path2):
            process = subprocess.Popen([path2, '-v', '|', 'more'], stdout=subprocess.PIPE)
        else:
            return
        version = process.communicate()[0].decode('UTF-8').replace('Mozilla Firefox', '').strip()
    else:
        return
    return version

def get_chrome_version(platform):
    """
    :return: the version of firefox installed on client
    """
    if platform == 'linux':
        with subprocess.Popen(['google-chrome', '--version'], stdout=subprocess.PIPE) as proc:
            version = proc.stdout.read().decode('utf-8').replace('Mozilla Firefox', '').strip()
    elif platform == 'mac':
        process = subprocess.Popen(['/Applications/Firefox.app/Contents/MacOS/firefox', '--version'], stdout=subprocess.PIPE)
        version = process.communicate()[0].decode('UTF-8').replace('Mozilla Firefox', '').strip()
    elif platform == 'win32':
        p = subprocess.Popen(["powershell.exe", "./../scripts/chromeversion.ps1"], stdout=subprocess.PIPE)
        result = p.communicate()[0]
        version = str(result).split("'")[1].split("\\")[0]
        return version

def get_msedge_version(platform):
    """
    :return: the version of firefox installed on client
    """
    if platform == 'linux':
        with subprocess.Popen(['google-chrome', '--version'], stdout=subprocess.PIPE) as proc:
            version = proc.stdout.read().decode('utf-8').replace('Mozilla Firefox', '').strip()
    elif platform == 'mac':
        process = subprocess.Popen(['/Applications/Firefox.app/Contents/MacOS/firefox', '--version'], stdout=subprocess.PIPE)
        version = process.communicate()[0].decode('UTF-8').replace('Mozilla Firefox', '').strip()
    elif platform == 'win32':
        p = subprocess.Popen(["powershell.exe", "./../scripts/msedgeversion.ps1"], stdout=subprocess.PIPE)
        result = p.communicate()[0]
        version = str(result).split("'")[1].split("\\")[0]
        return version

def uncompress(OS, file, directory):
    platform = OS
    if platform == 'win32':
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(directory)
    else:
        tar = tarfile.open(fileobj=file, mode='r:gz')
        tar.extractall(directory)
        tar.close()

def get_site_links(url):
    response = urlopen(url)
    bsObj = BeautifulSoup(response.read())
    download_links = bsObj.find_all("a")
    return download_links
    