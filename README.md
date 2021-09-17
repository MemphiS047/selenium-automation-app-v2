## Selenium (Python) Testing, Automation Program
### About
This program automates login process for most of the popular ecommerce sites as well as <br>
social media sites with a single generic login(url, acc_name, acc_password) function. Test the <br>
adding products to card process for some of the ecommerce sites. For testing and automation bs4 <br> 
and selenium used for scrapping and interacting with the web

### Driver
Since selenium needs driver installed and its path located in the system environment <br> 
this process is automated by  <code>driver.py</code>. To initialize a driver, create an instance of <br> 
the driver that will be used (Currently Chrome, Firefox, Edge available) - <code>chrome = Chrome()</code> then get <br> 
selenium web driver by simply calling - <code>driver = chrome.get_selenium_driver()</code> 

### Instructions
To install required packages run requirement.txt belove. By running <code>pip install -r requirements.txt</code> <br> 
via console 

        beautifulsoup4     == 4.9.3 
        certifi            == 2021.5.30 
        charset-normalizer == 2.0.4 
        idna               == 3.2 
        packaging          == 21.0 
        pip                == 21.1.1 
        pyparsing          == 2.4.7 
        PyYAML             == 5.4.1 
        requests           == 2.26.0 
        selenium           == 3.141.0
        setuptools         == 56.0.0
        soupsieve          == 2.2.1
        subprocess.run     == 0.0.8 
        urllib3            == 1.26.6

To run the test cases modify <code>app.py</code> by adding <code>goto_*</code> methods and redirecting trough pages <br>
To test cases for a ecommerce site (n11) you must login with the login() aforementioned. <br>
Then just run <code>python app.py</code> on the console. <br>

### Logging
Logging hold in the app.log file both driver logg and test logg is located inside it. <br>
Loggs can be viewed with timestamp and [test] or [driver] tags, also geckodriver creates <br>
its own geckodriver.log file as well.

### Test sytnax
To build tests cases testcases.yaml should be eddited according to yaml syntax and special <br>
"syntax" mimicks a programming language. Syntax is defined below
        
        goto type -<Type Name>  / This command redirects to one of the type represented as <Type Name>
        goto category -<Category Name> / This command redirects to one of the categorays of the  
                                                the selected type by 'goto type'
        back / Goes back
        add -<Product Name> / Adds product to specified category by 'goto category'
        login -email(username) -password / loggs in user to specified test destination 
       
Test destination defined on the testcases.yaml file also naming of the test cases also defined in the <br>
testcases.yaml file. To name test destination just write it accordingly to the resource in resource.yaml file <br>
and then write the name of the test case as a "child" according to yaml syntax. :
        
        test_destination :
                test_case_name :
                        <Commands here>

An example can be found in the testcase.yaml file.
                
