# linkedin_scraper/auth/login_manager.py
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import getpass
from linkedin_job_scraper.utils import constant as c
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class LoginManager:
    def __init__(self, driver):
        self.driver = driver

    def __prompt_email_password():
        u = input("Email: ")
        p = getpass.getpass(prompt="Password: ")
        return (u, p)

    def page_has_loaded(self):
        page_state = self.driver.execute_script('return document.readyState;')
        return page_state == 'complete'

    def login(self, email=None, password=None, cookie = None, timeout=10):
        if cookie is not None:
            return self._login_with_cookie(self.driver, cookie)
    
        if not email or not password:
            email, password = self.__prompt_email_password()
    
        self.driver.get("https://www.linkedin.com/login")
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
    
        email_elem = self.driver.find_element(By.ID,"username")
        email_elem.send_keys(email)
    
        password_elem = self.driver.find_element(By.ID,"password")
        password_elem.send_keys(password)
        password_elem.submit()
    
        if self.driver.current_url == 'https://www.linkedin.com/checkpoint/lg/login-submit':
            remember = self.driver.find_element(By.ID,c.REMEMBER_PROMPT)
            if remember:
                remember.submit()
    
        element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, c.VERIFY_LOGIN_ID)))
    
    def _login_with_cookie(self, cookie):
        self.driver.get("https://www.linkedin.com/login")
        self.driver.add_cookie({
            "name": "li_at",
            "value": cookie
        })
