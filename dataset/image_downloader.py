from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
from PIL import Image

# Setting selenium's driver and basic URLs
DRIVER_PATH = "NONE"
GOOGLE_IMAGES_URL = 'https://www.google.ca/imghp?hl=en&tab=ri&authuser=0&ogbl'
driver = webdriver.Chrome(DRIVER_PATH)
driver.get(GOOGLE_IMAGES_URL)
ImgSize = 256

##search bar html xpath
sb_xpath = '//*[@id="sbtc"]/div/div[2]/input'
box = driver.find_element_by_xpath(sb_xpath)

##close google's cookies premission
driver.find_element_by_xpath('//*[@id="L2AGLb"]/div').click()

##input and enter search result
SEARCH_BAR_TEXT = 'glitchcore aesthetic'
box.send_keys(SEARCH_BAR_TEXT)
box.send_keys(Keys.ENTER)
box = driver.find_element_by_xpath( '//*[@id="yDmH0d"]')

# Will keep scrolling down the webpage until it cannot scroll no more
last_height = driver.execute_script('return document.body.scrollHeight')
Scroll_flag = False
while Scroll_flag:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(2)
    new_height = driver.execute_script('return document.body.scrollHeight')
    try:
        driver.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div/div[5]/input').click()
        time.sleep(2)
    except:
        pass
    if new_height == last_height:
        break
    last_height = new_height    
    
for im_num in range(1, 30):
    image_xpath = f'//*[@id="islrg"]/div[1]/div[{str(im_num)}]/a[1]/div[1]/img'
    try:
        driver.find_element_by_xpath(image_xpath).click()
        full_im_xpath = f'//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img'
        SAVE_PATH = f':\yout\path\here\{str(im_num)}.png'
        driver.find_element_by_xpath(full_im_xpath).screenshot(SAVE_PATH)
        glitch_img = Image.open(SAVE_PATH)
        glitch_img  = glitch_img.resize((ImgSize, ImgSize))
        glitch_img.save(SAVE_PATH)
    except:
        pass




