import logging
import os
import re
from io import BytesIO
from sys import platform
from urllib.error import HTTPError
from urllib.request import urlopen
import sys
import yaml
from packaging import version
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.firefox.options import Options

from utils.app_utils import get_yaml_resource
from utils.driver_utils import (get_chrome_version, get_firefox_version,
                                get_msedge_version, get_site_links, uncompress)

"""
1.5. Drivers
Selenium requires a driver to interface with the chosen browser. Firefox, for example, requires geckodriver, 
which needs to be installed before the below examples can be run. 
Make sure it’s in your PATH, e. g., place it in /usr/bin or /usr/local/bin.
Failure to observe this step will give you an error selenium.common.exceptions.WebDriverException: 
Message: ‘geckodriver’ executable needs to be in PATH.
Other supported browsers will have their own drivers available. 
Links to some of the more popular browser drivers follow.
"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file = logging.FileHandler("app.log")
file.setLevel(logging.DEBUG)
file.setFormatter(logging.Formatter("%(asctime)3s:%(levelname)s:%(message)s",datefmt="%H:%M:%S"))
logger.addHandler(file)
logger.addHandler(logging.StreamHandler(sys.stdout))

class Driver():

    _OS = ""
    _driver_installed_path = ""
    _driver_install_url = ""
    _driver_version = ""
    _browser_version = ""
    _driverName = ""

    def __init__(self):
        self.set_os()

    def is_version_url_valid(self, url):
        """
        Check if version url is valid, if URL is not valid return False else return True
        """
        try:
            urlopen(url).getcode() != 200
            return True
        except HTTPError as err:
            logger.error(f"[driver] Can't reach url - {url} 404")
            return False

            
    def is_install_url_valid(self):
        """
        Checks the URL if its still accessible. 
        If URL not set then print message returns False, if url is not accessible returns False and prints message
        if response is 200 returns True
        """
        if(self._driver_install_url == None or self._driver_install_url == ""):
            logger.error("[driver] Driver install URL is not set. Set it with set_driver_install_url()")
            return False

        response = urlopen(self._driver_install_url)
        if(response.getcode() != 200):
            logger.error(f"[driver] Can't reach url - {self._driver_install_url} 404")
            return False

        if(response.getcode() == 200):
            logger.info("[driver] Install url is valid")
            return True

    def get_driver_filename(self):
        """
        Returns the drivers filename with its extension depending on the OS
        """
        if(self._OS == "win32"):
            return ".exe"
        return ""

    def set_driver_install_url(self):
        """
        Retrieves intall url links from yaml file according to driver name OS and version
        """
        with open("resource.yaml") as file:
            yaml_resource = yaml.safe_load(file)
            link = yaml_resource["install_links"][self._driverName][self._OS]
            self._driver_install_url = link.format(self._driver_version)
            logger.info("[driver] Driver install url is set via resource.yaml")

    def set_os(self):
        """
        Retrieves platform and sets instance _OS If not OS specified program exits with a message
        By defualt when a Driver instance is created _OS platform is specified.
        """
        if(platform.startswith('linux')):
            self._OS = 'linux'
            logger.info(f"[driver] OS attribute initialized to - {self._OS}")
        elif(platform.startswith('win32')):
            self._OS = 'win32'
            logger.info(f"[driver] OS attribute initialized to - {self._OS}")
        elif(platform.startswith('darwin')):
            self._OS = 'mac'
            logger.info(f"[driver] OS attribute initialized to - {self._OS}")
        else:
            logger.error("[driver] Couldn't specify the OS")
            logger.info("[driver] Exiting")
            exit()

    def set_browser_version(self, version):
        """
        Set browser version
        """
        self._browser_version = version
        logger.info(f"[driver] Web browser version - {self._browser_version}")

    def set_driver_system_path(self):
        """
        Sets driver installed path to system environement path
        """
        if(self._driver_installed_path == "" or self._driver_installed_path == None):
            logger.error("[driver] Driver installed path does not exist or couldn't find any installed driver")
            logger.info("[driver] Exiting...")
            exit()
        os.environ["Path"] += os.pathsep + self._driver_installed_path
        logger.info("[driver] Path set to installed driver...")

    def install_driver(self):
        """
        Before installing driver checks for installed driver versions, gets all driver version
        sets driver install url then installs driver 
        """
        if(self.is_install_url_valid()):
            driver_dir = os.path.join(
                os.path.abspath(os.getcwd()),
                f"{self._driver_version}"
            )
            try:
                os.mkdir(driver_dir)
            except FileExistsError as err:
                logger.warning("[driver] Directory already exists...")
                logger.info("[driver] Initializing driver path...")
                for name in os.listdir(driver_dir):
                    if(name.lower().endswith('.exe')):
                        logger.info(f"[driver] DRIVER LOCATED IN DIRECTORY (CWD): {driver_dir}")
                        logger.warning("[driver] System environment variable path did not set since driver is installed already")
                        self._driver_installed_path = os.path.join(driver_dir, name)
                        return os.path.join(driver_dir, name)
            logger.info(f"[driver] Installing {self._driverName} version {self._driver_version}....")
            logger.info(f"[driver] Installing to cwd - {driver_dir}")
            response = urlopen(self._driver_install_url)
            archive = BytesIO(response.read())
            uncompress(self._OS ,archive, driver_dir)
            self._driver_installed_path = os.path.join(driver_dir, self._driverName + self.get_driver_filename())
            logger.info(f"[driver] DRIVER INSTALLED IN DIRECTORY (CWD): {self._driver_installed_path}")
            self.set_driver_system_path()
            return os.path.join(driver_dir, self._driverName + self.get_driver_filename())
            
        else:
            logger.error("[driver] ERROR : Driver URL is not valid or couldn't install driver")
            logger.info("[driver] Exiting....")
            exit()

class Chrome(Driver):
    _webdriver = None
    def __init__(self):
        self._driverName = "chromedriver"
        self.set_os()
        self.set_driver_version()
        self.set_driver_install_url()
        self.install_driver()        
        logger.info("\n")
        
    def get_available_versions(self, print_versions=False):
        resource = get_yaml_resource("resource.yaml")
        url = resource["version_links"]["chrome"]
        version_lst = []
        if(self.is_version_url_valid(url)):
            download_links = get_site_links(url)
            for link in download_links:
                try:
                    if("chromedriver.storage" in link["href"]):
                        version = link["href"].split('/')[3].split('=')[1]
                        if(print_versions):
                            print(version)
                        version_lst.append(version)
                except:
                    pass
            return version_lst
        else:
            exit()

    def get_webdriver(self):
        try:
            driver = webdriver.Chrome(executable_path=self._driver_installed_path)
        except SessionNotCreatedException as err:
            logger.error("[driver] Session couldn't created due to following error -",err)
            logger.error("""
            [driver] By default Driver is created with the latest version
            For compatiblity specifiy version realted to your browsers verison
            """)
            logger.info("[driver] Exiting...")
            exit()
        return driver

    def set_driver_version(self):
        self.set_browser_version(get_chrome_version(self._OS))
        version_header = self._browser_version.split(".")[0]
        reg_exp = version_header + ".*"
        version_lst = self.get_available_versions()
        compatible_version = []
        for version in version_lst:
            try:
                match = re.search(reg_exp, version).string
                logger.info(f"[driver] Find compatible version - {version}")
                compatible_version.append(match) 
            except AttributeError as err:
                continue
        self._driver_version = compatible_version[0]

class Firefox(Driver):
    _webdriver = None
    def __init__(self):
        self._driverName = "geckodriver"
        self.set_os()
        self.set_driver_version()
        self.set_driver_install_url()
        self.install_driver() 
        logger.info("\n")

    def get_available_versions(self, print_versions=False):
        resource = get_yaml_resource("resource.yaml")
        url = resource["version_links"]["firefox"]
        version_lst = []
        if(self.is_version_url_valid(url)):
            download_links = get_site_links(url)
            for link in download_links:
                try:
                    if("releases/tag" in link["href"]):
                        version = link['href'].split('/')[5]
                        if(print_versions):
                            print(version)
                        version_lst.append(version)
                except:
                    pass
            return version_lst
        else:
            exit()

    def get_webdriver(self):
        try:
            options = Options()
            options.binary_location = r"C:\\PROGRA~1\\Mozilla Firefox\\firefox.exe"            
            driver = webdriver.Firefox(executable_path=self._driver_installed_path, firefox_options=options)
        except SessionNotCreatedException as err:
            logger.error("[driver] Session couldn't created due to following error -",err)
            logger.info("[driver] Exiting...")
            exit()
        return driver
       
    def set_driver_version(self):
        version_lst = self.get_available_versions()
        self.set_browser_version(get_firefox_version(self._OS))
        if(version.parse(self._browser_version) >= version.parse("60.0")):
            self._driver_version = "0.29.0"
            logger.info(f"[driver] Find compatible version - {self._driver_version}")
        elif(version.parse(self._browser_version) == version.parse("57.0")):
            self._driver_version = "0.25.0"
            logger.info(f"[driver] Find compatible version - {self._driver_version}")
        elif(version.parse(self._browser_version) == version.parse("55.0")):
            self._driver_version = "0.20.1"
            logger.info(f"[driver] Find compatible version - {self._driver_version}")
        elif(version.parse(self._browser_version) == version.parse("53.0")):
            self._driver_version = "0.18.0"
            logger.info(f"[driver] Find compatible version - {self._driver_version}")
        elif(version.parse(self._browser_version) == version.parse("52.0")):
            self._driver_version = "0.17.0"
            logger.info(f"[driver] Find compatible version - {self._driver_version}")
        else:
            logger.error("[driver] Could not set the driver version since ther are no compatible version for installed browser")
            return

class MSEdge(Driver):
    _webdriver = None
    def __init__(self):
        self._driverName = "msedgedriver"
        self.set_os()
        self.set_driver_version()
        self.set_driver_install_url()
        self.install_driver()
        logger.info("\n")

    def get_available_versions(self, print_versions=False):
        resource = get_yaml_resource("resource.yaml")
        url = resource["version_links"]["msedge"]
        version_lst = []
        if(self.is_version_url_valid(url)):
            download_links = get_site_links(url)
            for link in download_links:
                try:
                    if("msedgedriver.azureedge" in link["href"]):
                        version = link['href'].split('/')[3]
                        version_lst.append(version)
                        if(print_versions):
                            print(version)
                except:
                    pass
            return version_lst
        else:
            exit()

    def set_driver_version(self):
        self.set_browser_version(get_msedge_version(self._OS))
        version_header = self._browser_version.split(".")[0]
        reg_exp = version_header + ".*"
        version_lst = self.get_available_versions()
        compatible_version = []
        for version in version_lst:
            try:
                match = re.search(reg_exp, version).string
                logger.info(f"[driver] Find compatible version - {version}")
                compatible_version.append(match) 
            except AttributeError as err:
                continue
        self._driver_version = compatible_version[0]
    
    def get_webdriver(self):
        try:
            driver = webdriver.Edge(executable_path=self._driver_installed_path)
        except SessionNotCreatedException as err:
            logger.error("[driver] Session couldn't created due to following error -",err)
            logger.error("""
            [driver] By default Driver is created with the latest version
            For compatiblity specifiy version realted to your browsers verison
            """)
            logger.info("[driver] Exiting...")
            exit()
        return driver