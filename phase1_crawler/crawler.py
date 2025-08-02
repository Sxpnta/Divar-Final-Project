import time
import random 
from datetime import datetime 
import logging 
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy.orm import sessionmaker 
from .database import Base, engine
from .models import DivarAd
from sqlalchemy.exc import IntegrityError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#SQLalchemy 
Session = sessionmaker(bind=engine)
session = Session()


#Chrome Options 
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument("--headless")
options.add_experimental_option("detach", True)
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--window-size==1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--remote-debugging-port+9222")

driver = webdriver.Chrome(options=options)

try: 
    max_retries = 3
    for attempt in range(max_retries):
        try:
            driver.get("https://divar.ir/s/tehran/real-estate")
            logger.info(f"Attemp {attempt +1} to load page succeeded")
            time.sleep(5)
            break 
        except Exception as e:
            logger.error(f"Attempt {attempt +1} failed: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(5)
            
    max_pages= 5 
    current_page = 0 
    while current_page < max_pages:
        try:
            logger.info("waiting for ads to load on page")
            time.sleep(5)
            WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "kt-post-card__body")))
            ads = driver.find_elements(By.CLASS_NAME,"kt-post-card__body")
            logger.info(f"Found ads on page {current_page +1}:{len(ads)}")
            if not ads:
                logger.warning("No ads found with kt-post-card__body, checking for titles as fallback")
                WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h2.kt-post-card__title")))
                ads = driver.find_elements(By.CLASS_NAME, "kt-post-card__body")
                logger.info(f"Fallback found {len(ads)} ads")

            if not ads:
                logger.error("No ads detected after fallback - page may be blocked or misconfigured")
                break
        except:
            print("Timeout waiting for page to load.")
            driver.quit()
            exit()
        for ad in ads:
            try:
                title_elem = ad.find_element(By.CSS_SELECTOR, "h2.kt-post-card__title")
                title = title_elem.text if title_elem else "No title"
                logger.info(f"Processing ad with title: {title}")
                
                descriptions = ad.find_elements(By.CSS_SELECTOR, "div.kt-post-card__description")
                deposit = next((d.text for d in descriptions if "ودیعه" in d.text), "No deposit")
                rent = next((d.text for d in descriptions if "اجاره" in d.text), "No rent")
                price = f"{deposit} | {rent}" if "No deposit" not in deposit or "No rent" not in rent else "No price"
                region = ad.find_element(By.CSS_SELECTOR, ".kt-post-card__bottom-description").text
                posted_date = datetime.now()
                link = ad.find_element(By.XPATH, "../../..").find_element(By.TAG_NAME, "a").get_attribute("href")  
            except NoSuchElementException:
                print("Missing element in ad. Skipping...")
                continue
            except Exception as e:
                print(f"Error processing ad: {e}")
                continue    

#Duplicate Check
            if session.query(DivarAd).filter(DivarAd.link == link).first():
                print(f"Skipping duplicate: {link}")
                continue
        
#Ad Page
            driver.execute_script("window.open(arguments[0]);", link)
            driver.switch_to.window(driver.window_handles[1])
            WebDriverWait(driver, 90).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.kt-description-row__text"))
            )    
            description = driver.find_element(By.CSS_SELECTOR, "div.kt-description-row__text").text
            
        def get_detail(label):
            try:
                elements = driver.find_elements(By.CSS_SELECTOR,"div.kt-group-row-item")
                for el in elements:
                    if label in el.text:
                        return el.text.split("\n")[1]
                    return""
            except:
                return "" 
             
        
            rooms = get_detail("اتاق")
            rooms = int(rooms) if rooms.isdigit() else None
            area_detail = get_detail("متراژ")
            year_built = get_detail("سال ساخت")
            document_type = get_detail("سند")
#Save to DB
            new_ad = DivarAd(
            title = title,
            price = price,
            region = region,
            posted_date = posted_date,
            link=link,
            area = area_detail if area_detail else "No Area",
            year_built = year_built,
            document_type = document_type
        )
            try:
                session.add(new_ad)
                session.commit()
                logger.info(f"Saved ad: {title}") 
            except IntegrityError:
                session.rollback()
                logger.info(f"Duplicate ad skipped: {link}")
            except Exception as e:
                logger.error(f"Failed to save ad {link}: {e}")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(random.uniform(1,3))
#Close Ad
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='pagination-next']")
            next_button.click()
            WebDriverWait(driver, 60).until(EC.staleness_of(driver.find_elements(By.CLASS_NAME, "kt-post-card__body")[0]))
            time.sleep(random.uniform(1, 3))
            current_page += 1
            logger.info(f"Moved to page {current_page + 1}")
        except Exception as e:
            logger.info(f"No next page or error: {e}. Ending crawler.")
            break                          
finally:
        logger.info("Crawler finished.")
        driver.quit()
        session.close()
        


  


