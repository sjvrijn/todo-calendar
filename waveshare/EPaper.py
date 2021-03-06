from waveshare.epd2in7b import EPD, EPD_HEIGHT, EPD_WIDTH
from PIL import Image, ImageDraw, ImageFont
import textwrap
import time


def get_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


class EPaper:

    font_file = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'
    font_sizes = [10, 12, 14, 16, 18, 24]


    def __init__(self, debug=False):

        self.fonts = {
            size: ImageFont.truetype(self.font_file, size)
            for size in self.font_sizes
        }

        if not debug:
            self.interface = EPD()
            self.interface.init()
            self.interface.Clear(0xFF)
        self.asleep = False


    def show_image(self, img_name):
        pass


    def show_text(self, text, location=(0,0), size=18):
        if self.asleep:
            self.interface.init()
            self.asleep = False
        HBlackimage = Image.new('1', (EPD_HEIGHT, EPD_WIDTH), 255)  # 264*176
        HRedimage = Image.new('1', (EPD_HEIGHT, EPD_WIDTH), 255)  # 264*176
        drawblack = ImageDraw.Draw(HBlackimage)

        wrapped_text = textwrap.wrap(text, width=25)
        x, y = location

        for i, line in enumerate(wrapped_text):
            line_y = y + (size + 2)*i
            drawblack.text((x, line_y), line, font=self.fonts[size], fill=0)

        drawblack.text((0, 140), get_ip(), font=self.fonts[12], fill=0)
        drawblack.text((0, 155), "Updated: {}".format(time.strftime("%H:%M:%S")), font=self.fonts[12], fill=0)

        self.interface.display(self.interface.getbuffer(HBlackimage), self.interface.getbuffer(HRedimage))
        self.interface.sleep()
        self.asleep = True

    def clear(self):
        self.interface.Clear(0xFF)
        self.interface.sleep()
        self.asleep = True
