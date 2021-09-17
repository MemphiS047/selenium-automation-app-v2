import argparse
import logging
import sys
import time
from typing import Type

from selenium.common.exceptions import (ElementNotInteractableException,
                                        NoSuchElementException)
from selenium.webdriver.support import expected_conditions as EC
from utils.app_utils import get_yaml_resource

from driver import Chrome, Firefox, MSEdge

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file = logging.FileHandler("app.log")
file.setLevel(logging.DEBUG)
file.setFormatter(logging.Formatter("%(asctime)3s:%(levelname)s:%(message)s",datefmt="%H:%M:%S"))
logger.addHandler(file)
logger.addHandler(logging.StreamHandler(sys.stdout))

driver = Chrome()
driver = driver.get_webdriver()

def test_login(url, acc_name, acc_password):
    """
    Generic login function for automating log in 
    actions for various e-commerece sites social web sites
    via selenium. Driver retrieved via System Path and Path passed
    as argument to the webdriver. Only Firefox avaialable
    """
    driver.get(url)
    
    logger.info("[test] Waiting page to reload (4s.)")
    time.sleep(4)
    username_in, password_in = get_login_inputs()
    submit_element = get_login_submit()

    username_in.send_keys(acc_name)
    password_in.send_keys(acc_password)
    submit_element.click()

def get_login_inputs():
    form = driver.find_element_by_tag_name("form")
    if(form):
        logger.info("[test] Logging in via form - Selenium")
    try:
        username_in = form.find_element_by_xpath("//input[@type='text']")
        password_in = form.find_element_by_xpath("//input[@type='password']")
    except NoSuchElementException as err:
       logger.error("[test] Couldn't find any login element in the page")
       logger.info("[test] Exiting...")
       exit()
    return username_in, password_in

def get_login_submit():
    form = driver.find_element_by_tag_name("form")
    submit_element = None
    if(form):
        for element in ["button", "div", "input"]:
            try:
                logger.info(f"[test] //{element}[@type, 'submit']")
                submit_element = form.find_element_by_xpath(f"//{element}[@type='submit' or @id='loginButton']")
                return submit_element
            except NoSuchElementException as err:
                logger.error(f"[test] Couldn't find form/{element} with @type 'submit'")
                if(element == "input"):
                    logger.error("[test] Exiting..")
                    exit()
                continue
            
    else:
        logger.error("[test] Couldn't find any submit element")
        logger.info("[test] Exiting...")
        exit()
    return submit_element

def test_goto_product_type_n11(product_type_name):
    logger.info("[test] Waiting for page to releoad... (2s.)")
    time.sleep(2)
    element = driver.find_element_by_xpath(f"//li/a[contains(@title, '{product_type_name}')]")
    element.click()

def test_goto_category_n11(category_name):
    logger.info("[test] Waiting for page to releoad... (2s.)")
    time.sleep(2)
    driver.execute_script("arguments[0].click();", driver.find_element_by_xpath(f"//li/a[contains(@title, '{category_name}')]"))

def test_add_to_cart(product_name):
    logger.info("[test] Waiting for product page to load... (2s.)")
    time.sleep(2)
    element = driver.find_element_by_xpath(f"//h3[@class='productName ' and text()[contains(., '{product_name}')]]")
    element.click()
    logger.info("[test] Waiting for product page to load... (2s.)")
    time.sleep(2)
    add_to_cart = driver.find_element_by_class_name("product-add-cart")
    add_to_cart.click()

def test_back():
    logger.info("[test] Waiting for page to releoad... (2s.)")
    time.sleep(2)
    driver.back()


def command_parse(test_destination, test_case_name):
    testcases = get_yaml_resource("testcases.yaml")
    if(test_destination != "trendyol" and test_destination != "n11"):
        logger.error("[test] Defined test destination in testcases.yaml not legal")
        logger.info("[test] Only 'trendyol' and 'n11' is available as a test destination currently")
        logger.info("[test] Exiting...")
        exit()
    else:
        test_lst = testcases[test_destination][test_case_name]
        tmp = []
        for test in test_lst:
            tmp.append(test.split('-'))
        return tmp, test_destination



def build_test():
    build_pack = []
    test_lst, test_destination = command_parse("n11", "n11_add_to_card")
    test_links = get_yaml_resource("resource.yaml")["test_links"]
    if(test_destination == "n11"):
        url = test_links["n11"]
    else:
        url = test_links["trendyol"]
    logger.info("[test] Building the test case via testcases.yaml")
    for test in test_lst:
        if("login " in test):
            try:
                build_pack.append(test_login(url, test[1].replace(" ", ""), test[2]).replace(" ", ""))
            except AttributeError as err:
                pass
        if("goto type " in test):
            build_pack.append(test_goto_product_type_n11(test[1]))
        if("back" in test):
            build_pack.append(test_back())
        if("goto category " in test):
            build_pack.append(test_goto_category_n11(test[1]))
        if("add " in test):
            build_pack.append(test_add_to_cart(test[1]))
    
    for function in build_pack:
        try:
            function()
        except TypeError as err:
            continue
