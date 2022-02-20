# https://thepythonguru.com/decoding-captchas-using-python/
# https://blog.csdn.net/u011457798/article/details/84063963
# https://pillow.readthedocs.io/en/stable/handbook/concepts.html
# !pip show selenium pytesseract
import pytesseract
import base64

from io import BytesIO
from PIL import Image, ImageEnhance, ImageFilter
from operator import itemgetter


# 修改圖片的灰度
def convertGray(captcha): 
    captcha = captcha.convert('RGB') # 更改為RGB模式  #這裡也可以嘗試使用L
    # 
    enhancer = ImageEnhance.Color(captcha)
    enhancer = enhancer.enhance(0)
    enhancer = ImageEnhance.Brightness(enhancer)
    enhancer = enhancer.enhance(2)
    enhancer = ImageEnhance.Contrast(enhancer)
    enhancer = enhancer.enhance(8)
    enhancer = ImageEnhance.Sharpness(enhancer)
    enhancer = enhancer.enhance(20)
    # enhancer = enhancer.point(lambda x: 0 if x < 143 else 255) # 二值化圖像
    return enhancer

# 剔除噪點像素
def delete_spot(image):
    image = image.convert('L')
    data = image.getdata()
    w, h = image.size
    black_point = 0
    for x in range(1, w - 1):
        for y in range(1, h - 1):
            mid_pixel = data[w * y + x]  # 中央像素點像素值
            if mid_pixel < 50:  # 找出上下左右四個方向像素點像素值
                top_pixel = data[w * (y - 1) + x]
                left_pixel = data[w * y + (x - 1)]
                down_pixel = data[w * (y + 1) + x]
                right_pixel = data[w * y + (x + 1)]
                # 判斷上下左右的黑色像素點總個數
                if top_pixel < 10:
                    black_point += 1
                if left_pixel < 10:
                    black_point += 1
                if down_pixel < 10:
                    black_point += 1
                if right_pixel < 10:
                    black_point += 1
                if black_point < 1:
                    image.putpixel((x, y), 255)
                black_point = 0
    # images.show()
    return image

'''
二值化處理圖片
'''
def convert_binarization_image(image,threshold=140):
    image = image.convert('L')
    image = image.point(get_table(threshold), '1')
    # binarization_image = image.convert('1')
    return image

# 二值化,默認閾值 127
# 設定閾值threshold，畫素值小於閾值，取值0，畫素值大於閾值，取值1 
# # 閾值具體多少需要多次嘗試，不同閾值效果不一樣 
def get_table(threshold=127):
    table = []
    for i in  range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table

# https://blog.csdn.net/u011457798/article/details/84063963
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

def remove_bg(img):
    new_image = []
    for i in img.getdata():
        if i[:3][0] in range(80, 131) and i[:3][1] in range(80, 131) and i[:3][2] in range(80, 131):
            new_image.append(i)
        else:
            new_image.append((255, 255, 255))
    img.putdata(new_image)
    return img

def iterate(im, iteration):
    if iteration == 0:
        return im

    im = im.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(2)
    im = im.convert('1')

    return iterate(im, iteration-1)

# 保留數量第二多的 Pix
def getSecondMaxPixImg(captcha):
    im = captcha.convert("P")
    his = im.histogram()
    values = {}
    for i in range(256):
        values[i] = his[i]
    # Color	Number of pixels
    # for j,k in sorted(values.items(), key=itemgetter(1), reverse=True)[:10]:
    #     print(j,k)
    
    secondPix = sorted(values.items(), key=itemgetter(1), reverse=True)[1][0]
    im2 = Image.new("RGB",im.size, "white")
    temp = {}
    for x in range(im.size[1]):
        for y in range(im.size[0]):
            pix = im.getpixel((y,x))
            temp[pix] = pix
            if pix == secondPix: 
                im2.putpixel((y,x),pix)
    # im2.show()
    # im2.save("output.gif")
    return im2

if __name__ == '__main__':
    captcha = Image.open("getCaptcha.png")


    captcha = clear_image(captcha)
    # captcha = convert_binarization_image(captcha)
    captcha.show()

    value = captcha.getextrema()
    print(value)

    captcha = getSecondMaxPixImg(captcha)
    captcha.show()



    # captcha = captcha.convert('1')
    # captcha.show()

    # #轉化為灰度圖
    # captcha = convert_binarization_image(captcha)
    # captcha = convertGray(captcha)
    # captcha = delete_spot(captcha)
    # captcha.show()

    # captcha = ImageOps.invert(captcha)
    # captcha = captcha.convert('1')
    # captcha.show()
    # captcha = captcha.convert('L')
    # captcha.show()
    captcha = pytesseract.image_to_string(captcha, lang="eng").strip()
    print(f'captcha: {captcha}')