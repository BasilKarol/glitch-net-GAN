from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
from PIL import Image
from webdriver_manager.chrome import ChromeDriverManager

# Setting selenium's driver and basic URLs
EDGE_IMAGES_URL = 'https://www.bing.com/images/'

chromedriver = ChromeDriverManager().install()
driver = webdriver.Chrome(chromedriver)
driver.get(EDGE_IMAGES_URL)
ImgSize = 256

##close edges's cookies premission
time.sleep(2)
driver.find_element_by_xpath('//*[@id="bnp_btn_reject"]').click()

##search bar html xpath
sb_xpath = '//*[@id="sb_form_q"]'
box = driver.find_element_by_xpath(sb_xpath)

##input and enter search result
SEARCH_BAR_TEXT = 'glitchcore aesthetic'
box.send_keys(SEARCH_BAR_TEXT)
box.send_keys(Keys.ENTER)

# Will keep scrolling down the webpage until it cannot scroll no more
last_height = driver.execute_script('return document.body.scrollHeight')
Scroll_flag = True
while Scroll_flag:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(2)
    new_height = driver.execute_script('return document.body.scrollHeight')
    try:
        driver.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div/div[5]/input').click()
        time.sleep(2)
    except:
        pass
    try:
        driver.find_element_by_xpath('//*[@id="bop_container"]/div[2]/a').click()
    except:
        pass
    if new_height == last_height:
        break
    last_height = new_height    

im_index = 0
for im_num in range(1, 500):
    for im_column in range(1, 7):
        try:
            image_xpath = f'//*[@id="mmComponent_images_2"]/ul[{im_num}]/li[{im_column}]/div/div[1]/a/div/img'
            # driver.find_element_by_xpath(image_xpath).click()
            SAVE_PATH = f'D:\Python_Work\glitch_net\dataset\girls\{str(im_index)}.png'
            driver.find_element_by_xpath(image_xpath).screenshot(SAVE_PATH)

            im_index += 1

            # Trying to locate full size image's thumbnail instead of a preview:
            # try: 
            #     full_im_xpath = '//*[@id="mainImageWindow"]/div[2]/div/div/div/img'
            #     SAVE_PATH = f'D:\Python_Work\glitch_net\dataset\girls\{str(im_num)}.png'
            #     driver.find_element_by_xpath(full_im_xpath).screenshot(SAVE_PATH)
            # except Exception as error:
            #      print(f'full_im_xpath {im_num} error: {error}')

            glitch_img = Image.open(SAVE_PATH)
            glitch_img  = glitch_img.resize((ImgSize, ImgSize))
            glitch_img.save(SAVE_PATH)
        except:
            print(f'Error while trying to click ({im_num}, {im_column}) image')




