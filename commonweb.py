from robot.libraries.BuiltIn import BuiltIn
from selenium import webdriver
import os
import signal
import platform
import re
import requests

context = BuiltIn().get_library_instance('SeleniumLibrary')
# cur_dir = os.path.dirname(os.path.realpath(__file__)) + "/chromedriver"


def get_driver_path():
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    system = platform.system()
    print(system)
    if system == "Darwin":
        return cur_dir + "/drivers/mac/chromedriver"
    if system == "Windows":
        return cur_dir + "\\drivers\\windows\\chromedriver"
    else:
        return cur_dir + "/drivers/linux/chromedriver"


def start_chrome_browser(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1440,900")
    options.add_argument("--ignore-certificate-errors")
    context.create_webdriver('Chrome', options=options, executable_path=get_driver_path())
    context.go_to(url)


def start_chrome_headless_browser(url):
    # print cur_dir
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1440,900")
    options.add_argument("--ignore-certificate-errors")
    context.create_webdriver("Chrome", options=options, executable_path=get_driver_path())
    context.go_to(url)

def verify_element_color(locator, expected_color):
    element = context.find_element(locator)
    actual_color = element.value_of_css_property("background-color")
    # print (actual_color)
    if actual_color != expected_color:
        raise AssertionError("Element '%s' is not having expected color '%s'." % (locator,expected_color))


def start_chrome_browser_dir(url,dir):
    prefs = {
    "download.default_directory": dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True
    }
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', prefs)
    options.add_argument("--window-size=1440,900")
    options.add_argument("--ignore-certificate-errors")
    context.create_webdriver('Chrome', options=options, executable_path=get_driver_path())
    context.go_to(url)


def start_chrome_headless_browser_remote(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1440,900")
    options.add_argument("--ignore-certificate-errors")
    context.create_webdriver("Remote", options=options, command_executor="http://192.168.0.51:5566/wd/hub")
    context.go_to(url)


def start_chrome_headless_browser_dir(url,dir):
    prefs = {
    "download.default_directory": dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True
    }
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("window-size=1440,900")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_experimental_option('prefs', prefs)
    context.create_webdriver('Chrome', options=options, executable_path=get_driver_path())
    current_driver = context.driver
    enable_download_in_headless_chrome(current_driver,dir)
    context.go_to(url)


def enable_download_in_headless_chrome(driver, download_dir):
   #add missing support for chrome "send_command"  to selenium webdriver
   driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

   params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
   driver.execute("send_command", params)


def kill_all_browsers():
    current_driver = context.driver
    current_driver.close()
    current_driver.quit()


def terminate_all_browsers():
    current_driver = context.driver
    pid = get_current_process_id(current_driver)
    print(pid)
    current_driver.close()
    current_driver.quit()
    kill_chrome_process(pid)


def get_current_process_id(driver):
    process_id = int(driver.service.process.pid)
    return process_id


def kill_chrome_process(pid):
    try:
        os.kill(pid, signal.SIGTERM)
    except OSError:
        return False
    else:
        return True


def table_columns_should_be_correct(locator,column_list):
    column_names = column_list.split(';')
    column_names = [name.strip() for name in column_names]
    length = len(column_names)
    if not context.find_elements(locator + "//thead//th[1]//*[contains(@class,'ant-checkbox')]"):
        for i in range(1, length + 1):
            if len(column_names[i - 1]) > 0:
                context.find_element(locator + "//thead//th[" + str(i) + "]//*[text()='" + column_names[i-1] + "']").is_displayed()
    else:
        for i in range(2, length + 1):
            context.find_element(locator + "//thead//th[" + str(i) + "]//*[text()='" + column_names[i-2] + "']").is_displayed()

def replace_consecutive_space(text):
    text = re.sub('\s+',' ', text)
    return text

def get_ops_session(url, username, password):
    payload = {'username': username, 'password': password, 'type': 'account'}
    files = []
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)
    return response.headers['Set-Cookie'].split(';')[0]
