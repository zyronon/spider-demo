import base64
import os
import requests
from PIL import Image
import json


def jietu():
    os.system('adb shell screencap -p /sdcard/360/01.png')
    os.system('adb pull -p /sdcard/360/01.png')


def crop():
    # 打开一张图
    img = Image.open('01.png')
    # 图片尺寸
    img_size = img.size
    h = img_size[1]  # 图片高度
    w = img_size[0]  # 图片宽度
    print(h)
    print(w)
    x = 0.25 * w
    y = 0.16 * h
    w = 0.5 * w
    h = 0.2 * h

    # 开始截取
    # region = img.crop((x, y, x + w, y + h))
    region = img.crop((220, 400, 800, 1850))
    # 保存图片
    region.save("01_1.png")


data = []
count = 0
isContinue = True


def orc():
    f = open('01_1.png', 'rb')  # 二进制方式打开图文件
    # 参数image：图像base64编码
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=24.9eaf4c6327ee083b5f4f8549a256692d.2592000.1564385059.282335-16675198'
    img = base64.b64encode(f.read())
    params = {"image": img}
    # params = urllib.urlencode(params)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    resp = requests.post(url, data=params, headers=headers)
    print(resp.text)
    dictResp = json.loads(resp.text)  # 输出dict类型
    print(dictResp['words_result'])
    words = dictResp['words_result']
    for item in words:
        name = item['words']
        global isContinue
        if name == '照片':
            isContinue = False
        if name == '消毒剂':
            isContinue = False
        temp = {'name': item['words'], 'type': '有害垃圾'}
        data.append(temp)
    CMD_ToBottom = 'adb shell input swipe 1000 1500 1000 600'
    os.system(CMD_ToBottom)


def run():
    jietu()
    crop()
    orc()


# if count < 10:

while isContinue:
    print('当前第' + str(count) + '页')
    count += 1
    run()

with open('data.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)
