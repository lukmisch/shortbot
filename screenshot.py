from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image

screenshotDir = "ingredients"
screenWidth = 400
screenHeight = 800

def getPostScreenshots(post):
    print("Taking screenshots...")
    driver, wait = __setupDriver(post.url)
    if ((driver, wait) == (False, False)):
        return False
    if (__takeScreenshot(post.id, driver, wait) == False):
        return False
    driver.quit()
    return True

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def __takeScreenshot(post_id, driver, wait):
    concat_id = "t3_" + post_id
    search = wait.until(EC.presence_of_element_located((By.ID, concat_id)))
    driver.execute_script("window.focus();")

    filename = "ingredients/title.png"
    fp = open(filename, "wb")
    fp.write(search.screenshot_as_png)
    fp.close()
    return True

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def __setupDriver(url: str):
    o = webdriver.ChromeOptions()
    # o.add_argument("--user-data-dir=C:/Users/Luke/AppData/Local/Google/Chrome/User Data")
    # o.add_argument("--profile-directory=C:/Users/Luke/AppData/Local/Google/Chrome/User Data/Default")
    o.add_argument("--no-sandbox")
    o.add_argument("--disable-dev-shm-usage")
    #o.add_argument("--headless")
    o.add_argument("--enable-chrome-browser-cloud-management")
        
    # Provide the full path to chromedriver.exe or ensure it's in your PATH
    driver = webdriver.Chrome(options=o)
    wait = WebDriverWait(driver, 10)
    driver.set_window_size(width=screenWidth, height=screenHeight)
    driver.get(url)


    return driver, wait
