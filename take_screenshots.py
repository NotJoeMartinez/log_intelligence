import random, time, datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import os, math
from PIL import Image, ImageFont, ImageDraw 

MAX_TIMEOUT_SECONDS = 10

def main():
    ip_list_path="ips_with_webservers.txt"
    ip_list = randomize_ips(ip_list_path)
    run_driver(ip_list)


def run_driver(ip_list):
    browser = webdriver.Firefox()
    browser.set_page_load_timeout(MAX_TIMEOUT_SECONDS)
    ips_found = os.listdir("screenshots")
    ips_found = [foo[:-4] for foo in ips_found]
    for ip in ip_list:
        if ip not in ips_found:
            try:
                print(f"Getting {ip}")
                browser.get(f'http://{ip}')
                print("waiting")
                time.sleep(4)
                browser.save_screenshot(f'screenshots/{ip}.png')

                url_text = browser.current_url
                with open("urls.txt", "a") as f:
                    f.write(f"{url_text}\n")


                overlay_url(url_text, ip)
                print(f"saving screenshot to screenshots/{ip}.png")

            except TimeoutException:
                continue
            except:
                continue 
                

    browser.quit()

def overlay_url(url_text, ip):
    font_path= "fonts/LiberationMono-Regular.ttf"
    url_font = ImageFont.truetype(font_path, 33)
    my_image = Image.open(f"screenshots/{ip}.png")
    draw = ImageDraw.Draw(my_image)

    width, height = my_image.size

    center_of_pic = math.floor((width / 2))
    
    x, y = (width-center_of_pic, height-100)
    # xx, yy = (width-400, height-100)

    w, h = url_font.getsize(url_text)

    draw.rectangle((x, y, x + w, y + h), fill='black')
    draw.text((x, y), url_text, fill='white', font=url_font)   

    my_image.save(f"screenshots/{ip}.png")



def randomize_ips(ip_list_path):
    with open(ip_list_path, "r") as f:
        lines = f.readlines()
        ip_list = [ line.strip() for line in lines]
        random.shuffle(ip_list) 
        return ip_list



if __name__ == '__main__':
    main()