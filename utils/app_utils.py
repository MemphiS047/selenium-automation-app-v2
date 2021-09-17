from urllib.error import HTTPError
from urllib.request import Request, urlopen

import yaml

login_button_texts = ["giriş yap", "log in", "sign in"]
placeholder_texts = ["şifre", "email", "e-mail", "e-posta", "password", "username", "kullanıcı ismi", "adresi", "kullanıcı adı "]

def get_html(url):
    """
    Obtains the HTML from the url retrieved via argument
    if request not retrieved then pass Request with Headers as User Agent
    """
    req = Request(
        url, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    try:
        html = urlopen(req) 
    except HTTPError as err:
        return None
    return html

def get_login_form(form_element_lst):
    """
    Get form element from the lst of elements according 
    to number of input elements. If number of input is
    lower or equal to one it is not login form return None
    else it is login form return that form directly w/o 
    checking other forms
    """
    input_lst = []
    for form in form_element_lst:
        input_lst = form.find_elements_by_tag_name("input")
    if(len(input_lst) <= 1):
        return None
    else:
        return form

def get_submit_button(element):
    """ 
    Returns button <div> or <input> by searcing xpath type='submit' 
    and checks for text similarities from list. If true
    returns that div else returns None  
    """
    div_lst= element.find_elements_by_tag_name("div")

    x_path = "//*[@type='submit']"
    input_lst = element.find_elements_by_xpath(x_path)

    for div in div_lst:
        if(div.text.lower() in login_button_texts):
            return div

    for input_element in input_lst:
        if(input_element.get_attribute("title").lower() in login_button_texts):
            return input_element
    return None

def get_yaml_resource(file):
    with open(file) as f:
        yaml_resource = yaml.safe_load(f)
        return yaml_resource

def double_check_input(element_lst):
    """
    Checks if the inputs are username, eamil and password
    according to its both placeholder and type and placeholder_text
    similarities if it is specifeid input returns the element if no
    input found then returns empty list
    """
    new_element_lst = []
    for element in element_lst:
        placeholder = element.get_attribute("placeholder")
        type_attr = element.get_attribute("type")
        for text in placeholder_texts:
            if((placeholder.lower().find(text) >= 0) or 
            (type_attr != "hidden" and 
            (type_attr == "text" or type_attr == "password"))):
                if(element not in new_element_lst):
                    new_element_lst.append(element)
        
    return new_element_lst
