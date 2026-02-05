from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# ────────────────────────────────────────────────
# CONFIGURATION
# ────────────────────────────────────────────────

BASE_URL = "https://uatngl.manappuram.com/lead/#/login"

CREDENTIALS = {
    "username": "369343",
    "password": "soft1234"
}

# Timeouts (seconds)
SHORT_WAIT      = 2
MEDIUM_WAIT     = 4
LONG_WAIT       = 6
VERY_LONG_WAIT  = 12
DROPDOWN_WAIT   = 3


def main():
    driver = webdriver.Firefox()
    driver.maximize_window()

    wait = WebDriverWait(driver, 15)

    try:
        # ── Login ───────────────────────────────────────────────
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
        print("Login button clicked → waiting for next page...")
        time.sleep(LONG_WAIT)

        # ── Popup after login ───────────────────────────────────
        print("Clicking OK on popup...")
        ok_button = driver.find_element(
            By.XPATH,
            "//button[contains(@class, 'ant-btn-primary')]//span[normalize-space(.)='OK']"
        )
        ok_button.click()
        time.sleep(MEDIUM_WAIT)
        print("OK clicked → waiting after popup...")
        time.sleep(MEDIUM_WAIT)

        # ── Navigate to Create Lead ─────────────────────────────
        print("Clicking 'Create Lead' sidebar link...")
        create_lead_link = driver.find_element(
            By.XPATH,
            "//app-sidebar-nav-link-content[.//i[contains(@class, 'cil-user-plus')]]"
            "//text()[normalize-space(.)='Create Lead']/ancestor::a"
        )
        create_lead_link.click()
        print("'Create Lead' clicked → waiting for form...")
        time.sleep(SHORT_WAIT)

        # ── Lead Type ───────────────────────────────────────────
        print("Clicking Lead Type dropdown...")
        dropdown_control = driver.find_element(
            By.XPATH,
            "//nz-select[contains(@nzplaceholder, 'Select Lead Type')]//nz-select-top-control"
        )
        dropdown_control.click()

        print("Waiting for 'New Lead' option...")
        new_lead_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class, 'ant-select-item-option-content') and normalize-space(.)='New Lead']")
            )
        )
        new_lead_option.click()
        print("'New Lead' selected")
        time.sleep(1)

        # ── Applicant details ───────────────────────────────────
        print("Entering Applicant Name...")
        name_field = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@placeholder=\"Enter Applicant's Full Name\"]")
            )
        )
        name_field.clear()
        name_field.send_keys("Sakthi")
        time.sleep(SHORT_WAIT)

        print("Filling Mobile Numbers...")
        mobile_fields = wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//input[@placeholder=\"Enter Applicant's Mobile Number\"]")
            )
        )

        print(f"→ Found {len(mobile_fields)} mobile field(s)")

        if len(mobile_fields) >= 2:
            mobile_fields[0].clear()
            mobile_fields[0].send_keys("8883961112")
            time.sleep(SHORT_WAIT)

            mobile_fields[1].clear()
            mobile_fields[1].send_keys("8883961112")
            time.sleep(SHORT_WAIT)
            print("Both Mobile 1 and Mobile 2 filled")
        elif len(mobile_fields) == 1:
            print("WARNING: Only ONE mobile field visible")
            mobile_fields[0].clear()
            mobile_fields[0].send_keys("8883961111")
        else:
            print("ERROR: No mobile fields found!")
            driver.save_screenshot("mobile_fields_missing.png")

        # ── Lead Source ─────────────────────────────────────────
        print("Opening Lead Source dropdown...")
        source_dropdown = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//nz-select[@nzplaceholder='Select the lead source']//nz-select-top-control")
            )
        )
        source_dropdown.click()
        time.sleep(1.2)

        print("Selecting 'Own lead'...")
        own_lead_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class, 'ant-select-item-option-content') and normalize-space(.)='Own lead']")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'nearest', inline: 'center'});", own_lead_option)
        time.sleep(0.5)
        driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));", own_lead_option)
        time.sleep(0.3)
        own_lead_option.click()
        print("'Own lead' selected")
        time.sleep(1.5)

        # ── Lead Generator Mobile ───────────────────────────────
        print("Entering Lead Generator Mobile Number...")
        lg_mobile_field = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@placeholder=\"Enter LG Mobile Number\"]")
            )
        )
        lg_mobile_field.clear()
        lg_mobile_field.send_keys("6543210989")
        time.sleep(SHORT_WAIT)

        # ── Product Type & Loan Scheme ──────────────────────────
        print("Opening Product Type dropdown...")
        product_dropdown = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//nz-select[@nzplaceholder='Select product Type']//nz-select-top-control")
            )
        )
        product_dropdown.click()
        time.sleep(1.0)

        print("Selecting 'LAP' (Product Type)...")
        lap_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class, 'ant-select-item-option-content') and normalize-space(.)='LAP']")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", lap_option)
        time.sleep(0.4)
        lap_option.click()
        time.sleep(1.2)

        print("Opening Loan Scheme dropdown...")
        scheme_dropdown = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//nz-select[@nzplaceholder='Select the loan scheme']//nz-select-top-control")
            )
        )
        scheme_dropdown.click()
        time.sleep(1.0)

        print("Selecting 'LAP' (Loan Scheme)...")
        lap_scheme_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class, 'ant-select-item-option-content') and normalize-space(.)='LAP']")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", lap_scheme_option)
        time.sleep(0.4)
        lap_scheme_option.click()
        time.sleep(1.5)

        # ── Loan Amount, PIN, State, Branch ─────────────────────
        print("Entering Total Loan Amount Requested...")
        loan_amount_field = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@placeholder=\"Total Loan Amount Requested\"]")
            )
        )
        loan_amount_field.clear()
        loan_amount_field.send_keys("500000")
        time.sleep(SHORT_WAIT)

        print("Entering PIN Code...")
        pincode_field = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@placeholder=\"PIN Code\"]")
            )
        )
        pincode_field.clear()
        pincode_field.send_keys("600001")
        time.sleep(SHORT_WAIT)

        # State
        print("Opening State dropdown...")
        state_dropdown = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//nz-select[@nzplaceholder='Select State']//nz-select-top-control")
            )
        )
        state_dropdown.click()
        time.sleep(1.2)

        print("Typing 'Tamil Nadu'...")
        search_input = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//nz-select[@nzplaceholder='Select State']//input[contains(@class, 'ant-select-selection-search-input')]")
            )
        )
        search_input.clear()
        search_input.send_keys("Tamil Nadu")
        time.sleep(1.5)

        print("Selecting 'Tamil Nadu'...")
        tamil_nadu_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class, 'ant-select-item-option-content') and normalize-space(.)='Tamil Nadu']")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'nearest', inline: 'center'});", tamil_nadu_option)
        time.sleep(0.5)
        driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));", tamil_nadu_option)
        time.sleep(0.3)
        tamil_nadu_option.click()
        time.sleep(1.5)

        # Branch
        print("Opening Branch dropdown...")
        branch_dropdown = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//nz-select[@nzplaceholder='Select a branch']//nz-select-top-control")
            )
        )
        branch_dropdown.click()
        time.sleep(1.2)

        print("Typing 'KAMASHIPALAYAM'...")
        search_input = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//nz-select[@nzplaceholder='Select a branch']//input[contains(@class, 'ant-select-selection-search-input')]")
            )
        )
        search_input.clear()
        search_input.send_keys("KAMASHIPALAYAM")
        time.sleep(1.5)

        print("Selecting 'KAMASHIPALAYAM (100)'...")
        branch_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class, 'ant-select-item-option-content') and contains(., 'KAMASHIPALAYAM')]")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'nearest', inline: 'center'});", branch_option)
        time.sleep(0.5)
        driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));", branch_option)
        time.sleep(0.3)
        branch_option.click()
        time.sleep(1.5)

        # ── Submit ──────────────────────────────────────────────
        print("Clicking 'Add Lead' button...")
        add_lead_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@nztype='primary' and .//span[contains(., 'Add Lead')]]")
            )
        )

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_lead_button)
        time.sleep(0.4)
        driver.execute_script("arguments[0].click();", add_lead_button)
        print("JS click executed on Add Lead button")
        time.sleep(1.2)

        print("Current URL :", driver.current_url)
        print("Page title  :", driver.title)

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