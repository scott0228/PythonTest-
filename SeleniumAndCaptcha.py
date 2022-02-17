# 
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

def convert_img(img,threshold): 
    img = img.convert("L") 
    im1 = img.filter(ImageFilter.BLUR)
    im2 = img.filter(ImageFilter.MinFilter(3))
    im3 = img.filter(ImageFilter.MinFilter)  
    im1.show()
    im2.show()
    im3.show()
    # 處理灰度 
    pixels = img.load() 
    for x in range(img.width):
        for y in range(img.height): 
            if pixels[x, y] > threshold: 
                pixels[x, y] = 255
            else: 
                pixels[x, y] = 0 

    data = img.getdata()
    w,h = img.size
    count = 0
    for x in range(1,h-1):
        for y in range(1, h - 1):
            # 找出各个像素方向
            mid_pixel = data[w * y + x]
            if mid_pixel == 0:
                top_pixel = data[w * (y - 1) + x]
                left_pixel = data[w * y + (x - 1)]
                down_pixel = data[w * (y + 1) + x]
                right_pixel = data[w * y + (x + 1)]
                if top_pixel == 0:
                    count += 1
                if left_pixel == 0:
                    count += 1
                if down_pixel == 0:
                    count += 1
                if right_pixel == 0:
                    count += 1
                if count > 4:
                    img.putpixel((x, y), 0)
    return img

# 辨斷 Captcha
def getCaptcha(elem):
    img_base64 = elem.screenshot_as_base64
    captcha = Image.open(BytesIO(base64.b64decode(img_base64)))
    image = convert_img(captcha,140)
    
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
