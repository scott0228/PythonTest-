# 
# !pip show selenium pytesseract
import pytesseract
import base64

from io import BytesIO
from PIL import Image, ImageOps

if __name__ == '__main__':
    captcha = Image.open("getCaptcha.png").convert('L')
    # captcha = ImageOps.autocontrast(captcha)
    captcha = captcha.convert("L") 
    pixels = captcha.load() 
    for x in range(captcha.width):
        for y in range(captcha.height): 
            if pixels[x, y] > 140: 
                pixels[x, y] = 255
            else: 
                pixels[x, y] = 0 

    captcha = captcha.point(lambda x: 0 if x<140 else 255, "1")
    # width, height = captcha.size
    # out = captcha.resize((width*5, height*5), Image.NEAREST)

    captcha.show()
