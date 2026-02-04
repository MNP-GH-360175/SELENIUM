from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
import time

GECKO_DRIVER_PATH = r"D:\RAJENDRAN\AUTOMATION\SELENIUM\geckodriver.exe"
BASE_URL          = "https://uatngl.manappuram.com/lead/#/login"

CREDENTIALS = {
    "username": "369343",
    "password": "soft1234"
}

# Timeouts (in seconds)
SHORT_WAIT      = 2
MEDIUM_WAIT     = 4
LONG_WAIT       = 6
VERY_LONG_WAIT  = 12
DROPDOWN_WAIT   = 3      # time after clicking to open dropdown

def main():
    service = Service(executable_path=GECKO_DRIVER_PATH)
    driver = webdriver.Firefox(service=service)
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
        password_field.clear()
        password_field.send_keys(CREDENTIALS["password"])
        time.sleep(SHORT_WAIT)

        print("Clicking login button...")
        login_button = driver.find_element(
            By.XPATH,
            "//button[contains(., 'Login') and contains(@class, 'btn-warning')]"
        )
        login_button.click()
        print("Login button clicked → waiting for dashboard / next page...")
        time.sleep(LONG_WAIT)

        print("Clicking OK on popup...")
        driver.find_element(
            By.XPATH,
            "//button[contains(@class, 'ant-btn-primary')]//span[normalize-space(.)='OK']"
        ).click()
        time.sleep(MEDIUM_WAIT)
        print("OK clicked → waiting after popup close...")
        time.sleep(MEDIUM_WAIT)

        print("Clicking 'Create Lead' sidebar navigation link...")
        create_lead_link = driver.find_element(
            By.XPATH,
            "//app-sidebar-nav-link-content[.//i[contains(@class, 'cil-user-plus')]]//text()[normalize-space(.)='Create Lead']/ancestor::a"
        )
        create_lead_link.click()
        print("'Create Lead' clicked → waiting for lead creation form...")
        time.sleep(VERY_LONG_WAIT)

        # ────────────────────────────────────────────────
        #           LEAD CREATION STARTS HERE
        # ────────────────────────────────────────────────

        print("\n=== Starting Lead Creation ===\n")

        # 1–2. Select Lead Type → New Lead
        print("Clicking Lead Type dropdown...")
        driver.find_element(By.XPATH, "//nz-select[contains(@nzplaceholder, 'Select Lead Type')]//nz-select-top-control").click()
        time.sleep(DROPDOWN_WAIT)
        print("Selecting 'New Lead'...")
        driver.find_element(By.XPATH, "//nz-option[@title='New Lead' or .//span[contains(.,'New Lead')]]").click()
        time.sleep(SHORT_WAIT)

        # 3. Applicant Name
        print("Entering Applicant Name...")
        driver.find_element(By.XPATH, "//input[@placeholder=\"Enter Applicant's Full Name\"]").send_keys("Rajjen")
        time.sleep(SHORT_WAIT)

        # 4. Mobile Number 1
        print("Entering Mobile Number 1...")
        driver.find_element(By.XPATH, "(//input[@placeholder=\"Enter Applicant's Mobile Number\"])[1]").send_keys("6543210988")
        time.sleep(SHORT_WAIT)

        # 5. Mobile Number 2
        print("Entering Mobile Number 2...")
        driver.find_element(By.XPATH, "(//input[@placeholder=\"Enter Applicant's Mobile Number\"])[2]").send_keys("6543210988")
        time.sleep(SHORT_WAIT)

        # 6. Lead Source → Own lead
        print("Scrolling to Lead Source section...")
        driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(SHORT_WAIT)

        print("Clicking Lead Source dropdown...")
        driver.find_element(By.XPATH, "//nz-select[contains(., 'Own lead') or contains(@class, 'ng-tns-c149-12')]//nz-select-top-control").click()
        time.sleep(DROPDOWN_WAIT)
        print("Selecting 'Own lead'...")
        driver.find_element(By.XPATH, "//nz-option[@title='Own lead' or .//span[contains(.,'Own lead')]]").click()
        time.sleep(SHORT_WAIT)

        # 7. Scroll down
        print("Scrolling page down...")
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(SHORT_WAIT)

        # 8. Lead Generator Mobile Number
        print("Entering Lead Generator Mobile Number...")
        driver.find_element(By.XPATH, "//input[@placeholder=\"Enter LG Mobile Number\"]").send_keys("6543210988")
        time.sleep(SHORT_WAIT)

        # 9–10. Loan Type → LAP
        print("Clicking Loan Type (Product type) dropdown...")
        driver.find_element(By.XPATH, "//nz-select[contains(., 'Select Product type')]//nz-select-top-control").click()
        time.sleep(DROPDOWN_WAIT)
        print("Selecting 'LAP'...")
        driver.find_element(By.XPATH, "//nz-option[@title='LAP' or .//span[contains(.,'LAP')]]").click()
        time.sleep(SHORT_WAIT)

        # 11. Scroll down
        driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(SHORT_WAIT)

        # 12–13. Scheme → LAP
        print("Clicking Scheme dropdown...")
        driver.find_element(By.XPATH, "//nz-select[contains(., 'Select the loan scheme')]//nz-select-top-control").click()
        time.sleep(DROPDOWN_WAIT)
        print("Selecting 'LAP' in scheme...")
        driver.find_element(By.XPATH, "//nz-option[@title='LAP' or .//span[contains(.,'LAP')]]").click()
        time.sleep(SHORT_WAIT)

        # 14. Loan Amount Requested
        print("Entering Loan Amount Requested...")
        driver.find_element(By.XPATH, "//input[@placeholder='Total Loan Amount Requested']").send_keys("600000")
        time.sleep(SHORT_WAIT)

        # 15. Pincode
        print("Entering Pincode...")
        driver.find_element(By.XPATH, "//input[@placeholder='PIN Code']").send_keys("638314")
        time.sleep(SHORT_WAIT)

        # 16–17. State → Tamil Nadu
        print("Clicking State dropdown...")
        driver.find_element(By.XPATH, "//nz-select[.//nz-select-item[@title='Tamil Nadu']]//nz-select-top-control").click()
        time.sleep(DROPDOWN_WAIT)
        print("Selecting 'Tamil Nadu'...")
        driver.find_element(By.XPATH, "//nz-option[@title='Tamil Nadu' or .//span[contains(.,'Tamil Nadu')]]").click()
        time.sleep(SHORT_WAIT)

        # 18–19. Branch → KAMASHIPALAYAM
        print("Scrolling to Branch...")
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(SHORT_WAIT)

        print("Clicking Branch dropdown...")
        driver.find_element(By.XPATH, "//nz-select[.//nz-select-item[@title='KAMASHIPALAYAM']]//nz-select-top-control").click()
        time.sleep(DROPDOWN_WAIT)
        print("Selecting 'KAMASHIPALAYAM'...")
        driver.find_element(By.XPATH, "//nz-option[@title='KAMASHIPALAYAM' or .//span[contains(.,'KAMASHIPALAYAM')]]").click()
        time.sleep(SHORT_WAIT)

        # 20. Click Add Lead button
        print("Scrolling to Add Lead button...")
        driver.execute_script("window.scrollBy(0, 600);")
        time.sleep(SHORT_WAIT)

        print("Clicking 'Add Lead' button...")
        driver.find_element(By.XPATH, "//button[contains(@class, 'ant-btn-primary')]//span[contains(., 'Add Lead')]").click()
        time.sleep(VERY_LONG_WAIT)

        print("\nLead submission attempted.")
        print("Current URL:", driver.current_url)
        print("Page title:", driver.title)

        print("\nKeeping browser open for 90 seconds (check success message / error)...")
        time.sleep(90)

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