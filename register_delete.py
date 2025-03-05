
import unittest
import requests
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Setup desired capabilities and start Appium session
capabilities = dict(
    platformName='Android',
    automationName='UiAutomator2',
    deviceName='bafae455',
    app='/home/panco/testnew/panco.apk',
    appPackage='me.panco.app',
    appActivity='.MainActivity',
    adbExecTimeout=100000,  # Timeout is set to 60 seconds
)

appium_server_url = 'http://192.168.1.24:4723'
get_user_info_url = "https://api.pantel.me/a/get_user_info?$=bc4a32be16e8fff86487e32a26db9513&users=[{%22phone_number%22:%22+988888886500%22}]"


class TestAppium(unittest.TestCase):
    def setUp(self):
        
        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

    def tearDown(self):
        if self.driver:
            self.driver.quit()

    def test_delete_account(self):
        # Initial user registration check
        response = requests.get(get_user_info_url)
        data = response.json()
        if not data.get("result"):
            print("This number is not registered.")
        
        # Wait for the "Login or Register" button in guest mode
        self.check_for_guest_mode()

	    # # Locate the notification pop up and click button 
        # self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "permission_allow_button").click()
        
        # WebDriverWait(self.driver, 20).until(
        #     EC.presence_of_element_located(
        #         (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("اجازه دادن")'))
        # ).click()

        # Locate the test phone number input field using accessibility ID
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "phone_number_input"))
        ).send_keys("8888886500")
        
        # Locate the 'Next' button and click it
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "login_next_btn").click()

        #check if the number has already had an account or not 
        #hasn't had an account
            # Wait for OPT input field to load
        WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "input_1"))
            )
            # Fill the OTP input field
        otp_code = "36500"
        for i in range(5):
                self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, f"input_{i + 1}").send_keys(otp_code[i])

            #registration info 
        WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText")'))
            ).send_keys("mahsa")
        WebDriverWait(self.driver, 20).until(
                 EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@content-desc="textInput" and @text="نام خانوادگی"]'))
             ).send_keys("qa")
            
        WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "modal_buttons_box_footer"))
            ).click()
        print("account signed up")
        
        #key input    
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@content-desc="textInput" and @text="رمز عبور رو وارد کن"]'))
        ).send_keys("Qwer1234")
        
        WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="ورود به پنکو"]'))
            ).click()
        
        # After entering password, check if the user is logged in
        response = requests.get(get_user_info_url)
        data = response.json()
        
        if data.get("result"):
            print("This number login")
        # Check for the tour guid
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "خودم بلدم..."))
            ).click()
        except Exception as e:
            # If the pop-up is not found, proceed with the rest of the test
            print("No tour appeared.")
        
        # Check for the presence of the pop-up
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "pantel_modal_close_btn"))
            ).click()
        except Exception as e:
            print(f"Type of exception: {type(e).__name__}")
            # If the pop-up is not found, proceed with the rest of the test
            print("No pop-up appeared.")

        # Select profile
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "header_side_menu"))
        ).click()

        

        # Check for the presence of the pop-up for incoming call permission
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "deny_incoming_call_permission"))
            ).click()
        except Exception as e:
            # If the pop-up is not found, proceed with the rest of the test
            print("No pop-up appeared.")


        # Select setting menu
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "chat_box_container"))
        ).click()

        # Define the scrollable action with UiScrollable
        scroll_to_logout = ('new UiScrollable(new UiSelector().scrollable(true))'
                            '.scrollIntoView(new UiSelector().description("settings_logout_item"))')
        
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "settings_privacy_item"))
        ).click()
        print("privacy tab enterd")

        #select delete account setting
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "settings_delete_item"))
        ).click()

        #delete account
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "حذف همیشگی حساب کاربری"))
        ).click()

        #accept deletion
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "بله!"))
        ).click()
        print('delete completed')
        
        time.sleep(10)
        response = requests.get(get_user_info_url)
        data = response.json()
        print(data)

        
    # helper method
    def check_for_guest_mode(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("ورود یا ثبت‌نام")'))
            ).click()
        except Exception as e:
            print("Error checking guest mode; proceeding with login ...")


if __name__ == '__main__':
    unittest.main()