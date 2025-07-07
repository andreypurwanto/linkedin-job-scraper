import os
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from linkedin_job_scraper.client import LinkedInJobScraper
from datetime import datetime

# start
def get_driver(address='localhost'):
    options = webdriver.ChromeOptions()

    # Optional: headless
    options.add_argument("--headless=new")

    # Zoom Chrome to 30%
    options.add_argument("--force-device-scale-factor=0.2")
    # options.add_argument("--high-dpi-support=1")
    options.add_argument("--window-size=5760,3420")
    options.add_argument("--start-maximized")

    # Make sure to pass `options` here
    driver = webdriver.Remote(
        command_executor=f'http://{address}:4444/wd/hub',
        options=options,
        desired_capabilities=DesiredCapabilities.CHROME
    )
    return driver

# Usage
driver = get_driver()

try:
    linkedin_job_scraper = LinkedInJobScraper(driver)
    linkedin_job_scraper.login('a', 'b')
    result = linkedin_job_scraper.search_jobs_by_url('https://www.linkedin.com/jobs/search/?f_TPR=19&geoId=92000000&keywords=python&location=worldwide&refresh=true&start=1', description=True)
    
    os.makedirs("output", exist_ok=True)
    filename = f"output/linkedin_jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.close()
    driver.quit()