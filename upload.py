import time, os, random
from selenium import webdriver
from selenium.webdriver.common.by import By

titles = ["Like and Subscribe for more r/TwoSentenceHorror Daily!",
    "Like and Sub for more TwoSentenceHorror Daily!",
    "Subscribe for r/TwoSentenceHorror Daily!",
    "Daily r/TwoSentenceHorror - Like & Subscribe",
    "Like and Subscribe for TwoSentenceHorror Daily!",
    "Subscribe and Like for r/TwoSentenceHorror Daily!",
    "More r/TwoSentenceHorror Daily! Like and Subscribe",
    "TwoSentenceHorror Daily! Subscribe and Like",
    "Daily r/TwoSentenceHorror - Like & Subscribe",
    "Like & Subscribe - r/TwoSentenceHorror Daily!",
    "More r/TwoSentenceHorror Daily! Like and Subscribe",
    "Daily r/TwoSentenceHorror! Like and Subscribe",
    "For more r/TwoSentenceHorror Daily, Like and Subscribe!"
]

def upload():
    o = webdriver.ChromeOptions()
    o.add_argument("--log-level=3")
    o.add_argument("--user-data-dir=C:/Users/Luke/AppData/Local/Google/Chrome/User Data")
    o.add_argument("--profile-directory=Default")
    # o.add_argument("--headless")
    o.binary_location = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"

    for filename in os.listdir("shorts"):
        file_path = os.path.join("shorts", filename)
        print("Uploading ", file_path, "...")

        bot = webdriver.Chrome(options=o)

        bot.get("https://studio.youtube.com")
        time.sleep(3)
        upload_button = bot.find_element(By.XPATH, '//*[@id="upload-icon"]')
        upload_button.click()
        time.sleep(1)

        file_input = bot.find_element(By.XPATH, '//*[@id="content"]/input')
        abs_path = os.path.abspath(file_path)
        file_input.send_keys(abs_path)

        time.sleep(7)

        # Here we will change the title.
        textbox = bot.find_element(By.ID, "textbox")
        textbox.clear()
        textbox.send_keys(random.choice(titles))

        next_button = bot.find_element(By.XPATH, '//*[@id="next-button"]')
        for i in range(3):
            next_button.click()
            time.sleep(1)

        done_button = bot.find_element(By.XPATH, '//*[@id="done-button"]')
        done_button.click()
        time.sleep(5)
        bot.quit()
        time.sleep(5)
    return True