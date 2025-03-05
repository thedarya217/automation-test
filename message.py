import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

import selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.command import Command

# ارسال پیام و ارسال گیف و ارسال هدیه و پاک کردن چت از بخش گپ ها

capabilities = dict(
    platformName='Android',
    automationName='UiAutomator2',
    deviceName='DUM0219722005759',
    app='/home/panco/testnew/panco.apk',
    appPackage='me.panco.app',
    appActivity='.MainActivity',
    adbExecTimeout=100000,  # Timeout is set to 60 seconds
)

appium_server_url = 'http://192.168.1.24:4723'


class TestAppium(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

    def tearDown(self):
        if self.driver:
            self.driver.quit()

    def test_chat(self):
    
            # Locate the test phone number input field using accessibility ID
        WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "phone_number_input"))
            ).send_keys("8888886438")

            # Locate the 'Next' button and click it
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "login_next_btn").click()

        WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (AppiumBy.ACCESSIBILITY_ID, "login_with_code"))
            ).click()

            # Wait for OPT input field to load
        WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "input_1"))
            )
            # Fill the OTP input field
        otp_code = "36438"
        for i in range(5):
                self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, f"input_{i + 1}").send_keys(otp_code[i])

                # Check for the presence of the pop-up
        try:
            WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "pantel_modal_close_btn"))
                ).click()
        except:
                raise Exception(f'No pop-up appeared after login in homepage.')
        '''except Exception as e:
                print(f"Type of exception: {type(e).__name__}")
                # If the pop-up is not found, proceed with the rest of the test
                print("No pop-up appeared.")'''

            # Locate the test phone number input field using accessibility ID
        WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (AppiumBy.ACCESSIBILITY_ID, "header_search_button"))
            ).click()

            # ارسال پیام و گیف به شماره 6425
        WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "header_search_input"))
            ).send_keys("u6425")

        WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "active_status_کاربر"))
            ).click()

        WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "6425, u6425"))
            ).click()

        try:
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "deny_incoming_call_permission"))
                ).click()
        except:
                raise Exception(f'No pop-up appeared for incoming call permission.')

        WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (AppiumBy.ACCESSIBILITY_ID, "chat_box_container"))
            ).click()


            # Select profile
        WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "chat_footer_input"))
            ).send_keys("test massage")

            # Locate the 'Next' button and click it
        WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "chat_footer_sending_container"))
            ).click()

            # Select profile
        WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "chat_footer_input"))
            ).click()

            # Locate the 'Next' button and click it
        WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "chat_footer_open_emoji_btn"))
            ).click()

            # Locate the 'Next' button and click it
        WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "gifs"))
            ).click()
        
        scroll_to_gif = ('new UiScrollable(new UiSelector().scrollable(true))'
                 '.scrollIntoView(new UiSelector().description("گیف روحی, 500"))')
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, scroll_to_gif))
            ).click()
            # Locate the 'Next' button and click it
        #WebDriverWait(self.driver, 30).until(
         #       EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "گیف روحی, 500"))
          #  ).click()

            
            # Select profile
        WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "gif_sending_container"))
            ).click()

            # Select profile
        WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "chat_header_back"))
            ).click()

        #self.driver.back()
            # ارسال هدیه (هدیه یک قاب تستی است که همیشه باید باشد و تغییر نکند)
        WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "send_gift_container"))
            ).click()

            # Locate the 'Next' button and click it
        WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "پروفایل"))
            ).click()

        WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "محصولات بیشتر"))
            ).click()

            # Define the scrollable action with UiScrollable
        scroll_to_frame = ('new UiScrollable(new UiSelector().scrollable(true))'
                            '.scrollIntoView(new UiSelector().description("%50, فریم با حاشیه جدید ۲, 1, 2"))')
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, scroll_to_frame))
            ).click()

        WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "buy_gift_and_send"))
            ).click()

        WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "pantel_modal_close_btn"))
            ).click()
        
        self.driver.back()
        WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "bottom_tab_ChatList"))
            ).click()

            # #long press a chat
        element=WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "user_id_1639293969470751"))
                )
        
            # Perform a long press on the element
        self.driver.execute_script("mobile: longClickGesture", {
                "elementId": element.id,  # element ID to long-press
                "duration": 2000       # Duration in milliseconds (e.g., 2000 ms = 2 seconds)
                    })
            #delete chat
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "long_press_wall_remove_null"))
                ).click()
            
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "accept_delete_chat"))
                ).click()
            
            

        print("delete sucessfully")
   



if __name__ == '__main__':
    unittest.main()
