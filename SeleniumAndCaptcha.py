# TESSDATA_PREFIX 
# mkdir -p ~/tesseract/tessdata
# cd ~/tesseract/tessdata
# curl -O https://raw.githubusercontent.com/tesseract-ocr/tessdata/main/eng.traineddata
# export TESSDATA_PREFIX=~/tesseract/tessdata
# !pip show selenium pytesseract
import pytesseract
import base64

from io import BytesIO
from PIL import Image, ImageFilter

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException     

def clear_image(image):
    image = image.convert('RGB')
    width = image.size[0]
    height = image.size[1]
    noise_color = get_noise_color(image)
    
    for x in range(width):
        for y in  range(height):
            #清除邊框和干擾色
            rgb = image.getpixel((x, y))
            if (x == 0 or y == 0 or x == width - 1 or y == height - 1 
                or rgb == noise_color or rgb[1]>100):
                image.putpixel((x, y), (255, 255, 255))
    return image

def get_noise_color(image):
    for y in range(1, image.size[1] - 1):
        # 獲取第2列非白的顏色
        (r, g, b) = image.getpixel((2, y))
        if r < 255 and g < 255 and b < 255:
            return (r, g, b)

# 辨斷 Captcha
def getCaptcha(elem):
    img_base64 = elem.screenshot_as_base64
    captcha = Image.open(BytesIO(base64.b64decode(img_base64)))
    image = clear_image(captcha)
    image.show()

    # 存下來方便之後對照
    elem.screenshot('getCaptcha.png')

    captcha = pytesseract.image_to_string(image, lang="eng").strip()
    print(f'captcha: {captcha}')
    return captcha


if __name__ == '__main__':
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')  # 啟動無頭模式
    # driver = webdriver.Chrome(options=chrome_options)

    fireFoxOptions = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(options=fireFoxOptions)

    driver.get("https://cart.books.com.tw/member/login")
    driver.find_element(By.XPATH, '//*[@id="login_id"]').send_keys( "scott")
    elem = driver.find_element(By.CSS_SELECTOR, "#captcha_img > img:nth-child(1)")
    driver.find_element(By.XPATH, '//*[@id="captcha"]').send_keys(getCaptcha(elem))
    driver.close()
