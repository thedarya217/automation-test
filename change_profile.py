import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import requests

# Setup desired capabilities and start Appium session
capabilities = dict(
    platformName='Android',
    automationName='UiAutomator2',
    deviceName='bafae455',
    app='/home/panco/Downloads/panco3.apk',
    appPackage='me.panco.app',
    appActivity='.MainActivity',
    adbExecTimeout=100000,  # Timeout is set to 60 seconds
)

appium_server_url = 'http://192.168.1.228:4723'


class TestAppium(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

    def tearDown(self):
        if self.driver:
            self.driver.quit()

    def test_change_profile_by_gallery(self):
        # Wait for the "Login or Register" button in guest mode
        self.check_for_guest_mode()

	    # # Locate the notification pop up and click button 
        # self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "permission_allow_button").click()
        
        # WebDriverWait(self.driver, 20).until(
        #     EC.presence_of_element_located(
        #         (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("اجازه دادن")'))
        # ).click()

        user_id='1636288351910575'
        #get profile api
        api_url=f"https://api.pantel.me/a/get_profile_pic?$=a3197fe10e5c13dd59eb0efcf7de7464&user_id={user_id}"

        data=requests.get(api_url)
        if data.status_code == 200:
            res=data.json()
            print(res)
        else:
            print("no response was fetched.")
        media_id1=res.get("result",{}).get("media_id",{})

        # Locate the test phone number input field using accessibility ID
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "phone_number_input"))
        ).send_keys("8888886444")

        # Locate the 'Next' button and click it
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "login_next_btn").click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (AppiumBy.ACCESSIBILITY_ID, 'login_with_code'))
        ).click()

        # Wait for OPT input field to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "input_1"))
        )
        # Fill the OTP input field
        otp_code = "36444"
        for i in range(5):
            self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, f"input_{i + 1}").send_keys(otp_code[i])


        # Check for the presence of the pop-up
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "pantel_modal_close_btn"))
            ).click()
        except Exception as e:
            print(f"Type of exception: {type(e).__name__}")
            # If the pop-up is not found, proceed with the rest of the test
            print("No pop-up appeared.")

        # Select header side menu
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "header_side_menu"))
        ).click()

        # Check for the presence of the pop-up for incoming call permission
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "deny_incoming_call_permission"))
            ).click()
        except Exception as e:
            # If the pop-up is not found, proceed with the rest of the test
            print("No pop-up appeared.")


        # Select profile setting menu
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "ویرایش پروفایل"))
        ).click()

        #press image
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "change_profile_picture_btn"))
        ).click()

        #select photo from gallary
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "profile_modal_gallery_container"))
        ).click()


        #select a photo from gallery
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (AppiumBy.XPATH, '(//android.widget.ImageView[@resource-id="com.google.android.providers.media.module:id/icon_thumbnail"])[1]'))
        ).click()
        print("a photo selected")

        #select picture
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Crop"))
        ).click()

        #fetch data after change of profile
        data2=requests.get(api_url)
        if data2.status_code == 200:
            res2=data2.json()
            print(res2)
        else:
            print("no response was fetched.")
        
        media_id2=res2.get("result",{}).get("media_id",{})
        print(media_id1)
        print(media_id2)

        if media_id1 == media_id2:
            print("profile picture did not change!")
        else:
            print(" sucessfully a photo from gallery selected.")

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "save_profile_btn_false"))
        ).click()

    # helper method
    def check_for_guest_mode(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("ورود یا ثبت‌نام")'))
            ).click()
        except Exception as e:
            print("Error checking guest mode; proceeding with login ...")

    '''def test_signup(self):
        # Wait for the "Login or Register" button using its text
        try:
            login_or_register_button = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("ورود یا ثبت‌نام")'))
            ).click()
        except Exception as e:
            # If the button is not found, it may indicate that we are not in guest mode
            print("Login or Register button not found; proceeding with login...")

        # Locate the test phone number input field using accessibility ID
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "phone_number_input"))
        ).send_keys("8888886438")

        # Locate the 'Next' button and click it
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "login_next_btn").click()'''


if __name__ == '__main__':
    unittest.main()