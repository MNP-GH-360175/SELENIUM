from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import Select
import time

GECKO_DRIVER_PATH = r"D:\RAJENDRAN\AUTOMATION\SELENIUM\geckodriver.exe"
BASE_URL          = "https://uatngl.manappuram.com/lead/#/login"

CREDENTIALS = {
    "username": "369343",
    "password": "soft1234"
}

# Timeouts (in seconds)
SHORT_WAIT   = 2
MEDIUM_WAIT  = 4
LONG_WAIT    = 6

def main():
    service = Service(executable_path=GECKO_DRIVER_PATH)
    driver = webdriver.Firefox()
    driver.maximize_window()

    try:
        print("Opening login page...")
        driver.get(BASE_URL)
        time.sleep(MEDIUM_WAIT)
        
        print("Entering username...")
        username_field = driver.find_element(By.NAME, "user")
        username_field.clear()
        username_field.send_keys(CREDENTIALS["username"])
        time.sleep(SHORT_WAIT)

        print("Entering password...")
        password_field = driver.find_element(By.NAME, "password")
        #driver.find_element(By.XPATH, "//input[@type='password']")
        password_field.clear()
        password_field.send_keys(CREDENTIALS["password"])
        time.sleep(SHORT_WAIT)

        print("Clicking login button...")
        
        login_button = driver.find_element( By.XPATH, "//button[contains(., 'Login') and contains(@class, 'btn-warning')]" )
        
        login_button.click()
        print("Login button clicked → waiting for dashboard / next page...")
        time.sleep(LONG_WAIT)
        
        print("Clicking OK on popup...")
        driver.find_element(By.XPATH, "//button[contains(@class, 'ant-btn-primary')]//span[normalize-space(.)='OK']").click()
        time.sleep(MEDIUM_WAIT)
        print("OK clicked → waiting after popup close...")
        time.sleep(MEDIUM_WAIT)
        
        print(f"Current URL after login: {driver.current_url}")
        print(f"Page title: {driver.title}")

        print("\nBrowser will stay open for 6 seconds...")
        time.sleep(6)
        

        
    except Exception as e:
        print("\nERROR occurred:")
        print(str(e))
        timestamp = int(time.time())
        driver.save_screenshot(f"error_{timestamp}.png")
        print(f"Screenshot saved → error_{timestamp}.png")

    finally:
        driver.quit()
        print("Browser closed.")


if __name__ == "__main__":
    main()