import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

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

appium_server_url = 'http://192.168.1.19:4723'


class TestAppium(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

    def tearDown(self):
        if self.driver:
            self.driver.quit()

    def test_login_with_opt(self):
        # Wait for the "Login or Register" button in guest mode
        self.check_for_guest_mode()

        # Locate the test phone number input field using accessibility ID
        WebDriverWait(self.driver, 10).until(
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
            WebDriverWait(self.driver, 20).until(
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

        # Perform the scroll and find the logout button
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, scroll_to_logout))
        ).click()

        # Accept logout
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "accept_log_out"))
        ).click()

    # helper method
    def check_for_guest_mode(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (AppiumBy.ACCESSIBILITY_ID, "login_with_code"))
            ).click()
        except Exception as e:
            print("Error checking guest modde; proceeding with login ...")


if __name__ == '__main__':
    unittest.main()
