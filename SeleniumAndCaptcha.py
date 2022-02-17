#!pip show selenium pytesseract
import pytesseract
import base64

from io import BytesIO
from PIL import Image

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException     

# 辨斷 Captcha
def getCaptcha(elem):
    img_base64 = elem.screenshot_as_base64
    image = Image.open(BytesIO(base64.b64decode(img_base64)))
    # 存下來方便之後對照
    elem.screenshot('getCaptcha.png')

    captcha = pytesseract.image_to_string(image, lang="eng").strip()
    print(f'captcha: {captcha}')
    return captcha


if __name__ == '__main__':
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')  # 啟動無頭模式
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://www.jihsun.com.tw/")