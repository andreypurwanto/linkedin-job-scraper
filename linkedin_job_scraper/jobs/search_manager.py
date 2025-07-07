# linkedin_scraper/jobs/search_manager.py
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import randint
from linkedin_job_scraper.utils.logger import logger

class SearchManager:
    def __init__(self, driver):
        self.driver = driver

    def search_by_url(self, url, description=False):
        self.driver.get(url)
        time.sleep(1)
        logger.info(f'Searching jobs with description {description} from URL: {url}')
        job_cards =  self.__get_job_cards_from_search_result()
        jobs_desc = []
        if description:
            jobs_desc = self.__get_job_descriptions_from_search(job_cards)
        res = {
            "job_cards": job_cards,
            "jobs_desc": jobs_desc
        }
        return res
    
    def __get_job_cards_from_search_result(self):
        res = []
        job_cards = self.driver.find_elements(By.CSS_SELECTOR, "li.scaffold-layout__list-item")
        for card in job_cards:
            try:
                job_id = card.get_attribute("data-occludable-job-id") or "N/A"

                # Job title and URL
                try:
                    title_elem = card.find_element(By.CSS_SELECTOR, "a.job-card-container__link")
                    title = title_elem.text.strip()
                    job_url = title_elem.get_attribute("href")
                except:
                    title, job_url = None, None

                # Company
                try:
                    company = card.find_element(By.CSS_SELECTOR, "div.artdeco-entity-lockup__subtitle span").text.strip()
                except:
                    company = None

                # Location
                try:
                    location = card.find_element(By.CSS_SELECTOR, "ul.job-card-container__metadata-wrapper li span").text.strip()
                except:
                    location = None

                # Posted time
                try:
                    posted_time = card.find_element(By.CSS_SELECTOR, "time").text.strip()
                except:
                    posted_time = None

                # Easy Apply
                try:
                    card.find_element(By.XPATH, ".//*[contains(text(), 'Easy Apply')]")
                    easy_apply = True
                except:
                    easy_apply = False

                # Output or collect result
                res.append({
                    "job_id": job_id,
                    "title": title,
                    "company": company,
                    "location": location,
                    "job_url": job_url,
                    "posted": posted_time,
                    "easy_apply": easy_apply
                })

            except Exception as e:
                # LOG.error(f"Error parsing job card (job_id={job_id if 'job_id' in locals() else 'unknown'}): {e}")
                continue  # Skip to next card

            finally:
                time.sleep(randint(1, 3))  # Random sleep to avoid detection

        return res
    
    def __click_from_search(self, job_id):
        # LOG.info(f'click_from_search {job_id}')
        # Wait until the job card is present
        job_card = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'div[data-job-id="{job_id}"]'))
        )

        # Scroll into view (optional but helpful)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", job_card)

        # Click the card
        job_card.click()

    def __get_description_from_search_click(self):
        # Wait for the description block to appear
        desc_elem = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.mt4 > p[dir='ltr']"))
        )

        # Get the full visible text
        description = desc_elem.text.strip()

        return description
    
    def __get_job_descriptions_from_search(self, job_cards):
        jobs_desc  = []
        for job_card in job_cards:
            job_id = job_card['job_id']
            logger.info(f'Processing job id: {job_id}')
            self.__click_from_search(job_id)
            desc = self.__get_description_from_search_click()
            jobs_desc.append({
                "job_id": job_id,
                "desc": desc
            })
            time.sleep(randint(1, 3))  # Random sleep to avoid detection
            
        return jobs_desc