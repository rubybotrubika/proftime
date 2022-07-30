from PIL import Image, ImageFont, ImageDraw
from datetime import datetime
from pytz import timezone
import os

def cr_image(text):
    image = Image.open(os.getcwd() + "/photo.jpg")
    W, H = image.size
    dw = ImageDraw.Draw(image)
    
    Font = ImageFont.truetype(font="digital.ttf", size=450)
    wt, ht = dw.textsize(text, font=Font)
    
    border_size , border_color = 3 , 'black'
    
    dw.text(((W - wt) / 2 - border_size, (H - ht) / 2 - border_size), text, font=Font, fill=border_color)
    dw.text(((W - wt) / 2 + border_size, (H - ht) / 2 - border_size), text, font=Font, fill=border_color)
    dw.text(((W - wt) / 2 - border_size, (H - ht) / 2 + border_size), text, font=Font, fill=border_color)
    dw.text(((W - wt) / 2 + border_size, (H - ht) / 2 + border_size), text, font=Font, fill=border_color)
    
    dw.text(((W - wt) / 2, (H - ht) / 2), text, font=Font, fill='white')
    
    image.save('time_image.jpg')
    
def get_time():
	return datetime.now(timezone('Asia/tehran')).strftime('%H:%M')
	
def del_image():
    os.remove('time_image.jpg')