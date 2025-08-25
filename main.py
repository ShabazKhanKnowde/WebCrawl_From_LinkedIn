from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

app = FastAPI()


class WebsiteRequest(BaseModel):
    website: str


def get_linkedin_url(website: str):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(website)

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "linkedin.com")]'))
            )
        except:
            pass

        social_links = driver.find_elements(By.XPATH, '//a[contains(@href, "linkedin.com")]')

        if social_links:
            linkedin_url = social_links[0].get_attribute("href")
            return {"linkedin_url": linkedin_url}
        else:
            return {"linkedin_url": None, "message": "LinkedIn URL not found"}

    except Exception as e:
        return {"error": str(e)}
    finally:
        driver.quit()


@app.post("/get-linkedin")
def extract_linkedin(data: WebsiteRequest):
    result = get_linkedin_url(data.website)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result
