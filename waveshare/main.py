#!/usr/bin/python
# -*- coding:utf-8 -*-

import epd2in7b
import time
from PIL import Image, ImageDraw, ImageFont
import traceback


def hello_horizontal(epd):
    # Drawing on the Horizontal image
    HBlackimage = Image.new('1', (epd2in7b.EPD_HEIGHT, epd2in7b.EPD_WIDTH), 255)  # 264*176
    HRedimage = Image.new('1', (epd2in7b.EPD_HEIGHT, epd2in7b.EPD_WIDTH), 255)  # 264*176

    # Horizontal
    print("Drawing")
    drawblack = ImageDraw.Draw(HBlackimage)
    drawred = ImageDraw.Draw(HRedimage)
    font24 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 24)
    drawblack.text((10, 0), 'hello world', font=font24, fill=0)
    drawblack.text((10, 20), '2.7inch e-Paper', font=font24, fill=0)
    drawblack.text((150, 0), u'微雪电子', font=font24, fill=0)
    drawblack.line((20, 50, 70, 100), fill=0)
    drawblack.line((70, 50, 20, 100), fill=0)
    drawblack.rectangle((20, 50, 70, 100), outline=0)
    drawred.line((165, 50, 165, 100), fill=0)
    drawred.line((140, 75, 190, 75), fill=0)
    drawred.arc((140, 50, 190, 100), 0, 360, fill=0)
    drawred.rectangle((80, 50, 130, 100), fill=0)
    drawred.chord((200, 50, 250, 100), 0, 360, fill=0)
    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRedimage))


def hello_vertical(epd):
    # Drawing on the Vertical image
    LBlackimage = Image.new('1', (epd2in7b.EPD_WIDTH, epd2in7b.EPD_HEIGHT), 255)  # 176*264
    LRedimage = Image.new('1', (epd2in7b.EPD_WIDTH, epd2in7b.EPD_HEIGHT), 255)  # 176*264
    # Vertical
    drawblack = ImageDraw.Draw(LBlackimage)
    drawred = ImageDraw.Draw(LRedimage)
    font18 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 18)
    drawblack.text((2, 0), 'hello world', font=font18, fill=0)
    drawblack.text((2, 20), '2.7inch epd', font=font18, fill=0)
    drawblack.text((20, 50), u'微雪电子', font=font18, fill=0)
    drawblack.line((10, 90, 60, 140), fill=0)
    drawblack.line((60, 90, 10, 140), fill=0)
    drawblack.rectangle((10, 90, 60, 140), outline=0)
    drawred.line((95, 90, 95, 140), fill=0)
    drawred.line((70, 115, 120, 115), fill=0)
    drawred.arc((70, 90, 120, 140), 0, 360, fill=0)
    drawred.rectangle((10, 150, 60, 200), fill=0)
    drawred.chord((70, 150, 120, 200), 0, 360, fill=0)
    epd.display(epd.getbuffer(LBlackimage), epd.getbuffer(LRedimage))


def image_1(epd):
    print("read bmp file")
    HBlackimage = Image.open('2in7b-b.bmp')
    HRedimage = Image.open('2in7b-r.bmp')
    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRedimage))


def image_2(epd):
    print("read bmp file on window")
    blackimage1 = Image.new('1', (epd2in7b.EPD_HEIGHT, epd2in7b.EPD_WIDTH), 255)  # 298*126
    redimage1 = Image.new('1', (epd2in7b.EPD_HEIGHT, epd2in7b.EPD_WIDTH), 255)  # 298*126
    newimage = Image.open('100x100.bmp')
    blackimage1.paste(newimage, (50, 10))
    epd.display(epd.getbuffer(blackimage1), epd.getbuffer(redimage1))


def run_demo():
    try:
        epd = epd2in7b.EPD()
        epd.init()
        print("Clear...")
        epd.Clear(0xFF)

        hello_horizontal(epd)
        time.sleep(2)

        hello_vertical(epd)
        time.sleep(2)

        image_1(epd)
        time.sleep(2)

        image_2(epd)
        epd.sleep()

    except:
        print(f'traceback.format_exc():\n'
              f'{traceback.format_exc()}')
        exit()


if __name__ == "__main__":
    run_demo()