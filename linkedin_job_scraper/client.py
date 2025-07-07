# linkedin_job_scraper/client.py
from linkedin_job_scraper.auth.login_manager import LoginManager
from linkedin_job_scraper.jobs.search_manager import SearchManager

class LinkedInJobScraper:
    def __init__(self, driver):
        self.driver = driver
        self.login_manager = LoginManager(driver)
        self.search_manager = SearchManager(driver)

    def login(self, username, password, **kwargs):
        self.login_manager.login(username, password)

    def search_jobs_by_url(self, url, description=False, **kwargs):
        return self.search_manager.search_by_url(url, description=description)