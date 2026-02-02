from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import Select
import time


GECKO_DRIVER_PATH = r"D:\RAJENDRAN\AUTOMATION\SELENIUM\geckodriver.exe"
BASE_URL          = "https://uatngl.manappuram.com/los/#/login"

CREDENTIALS = {
    "username": "369343",
    "password": "soft1234"
}

LEAD_ID_TO_SELECT = "L0100000731"          

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
        driver.find_element(By.NAME, "username").send_keys(CREDENTIALS["username"])
        time.sleep(SHORT_WAIT)

        print("Entering password...")
        driver.find_element(By.XPATH, "//input[@type='password']").send_keys(CREDENTIALS["password"])
        time.sleep(SHORT_WAIT)

        print("Clicking login button...")
        driver.find_element(By.XPATH, "(//button)[2]").click()
        time.sleep(LONG_WAIT)

        print("Clicking OK on popup...")
        driver.find_element( By.XPATH, "//button[contains(@class, 'ant-btn-primary')]//span[normalize-space(.)='OK']" ).click()
        time.sleep(MEDIUM_WAIT)

        print("Opening 'Loan Applications' menu...")
        driver.find_element(By.XPATH, "//div[contains(@class, 'nav_link')]//span[text()='Loan Applications']").click()
        time.sleep(LONG_WAIT)

        print("Selecting sub-menu 'Loan Application'...")
        driver.find_element( By.XPATH,"//li[contains(@class, 'navsub_link')]//span[normalize-space(.)='Loan Application']").click()
        time.sleep(LONG_WAIT)

        print("Clicking '+ Create New Application'...")
        driver.find_element( By.XPATH, "//button[contains(@class, 'primary-btn') and contains(., 'Create New Application')]").click()
        time.sleep(LONG_WAIT)

        print("Selecting product: MSME & ALLIED")
        Select(driver.find_element(By.CSS_SELECTOR, "select[formcontrolname='productId']")) \
            .select_by_visible_text("MSME & ALLIED")
        time.sleep(MEDIUM_WAIT)

        print(f"Selecting Lead ID: {LEAD_ID_TO_SELECT}")
        driver.find_element(By.CSS_SELECTOR, "input.ant-select-selection-search-input[autocomplete='off']").click()
        time.sleep(SHORT_WAIT)
        driver.find_element(By.XPATH, f"//div[contains(@class, 'ant-select-item-option-content') and contains(., '{LEAD_ID_TO_SELECT}')]").click()
        time.sleep(MEDIUM_WAIT)

        print("Clicking Confirm button...")
        driver.find_element( By.XPATH, "//button[contains(@class, 'btn-success') and .//span[contains(., 'Confirm')]]").click()
        time.sleep(LONG_WAIT)

        print("Selecting Loan Type: LAP")
        Select(driver.find_element(By.CSS_SELECTOR, "select[formcontrolname='loanTypeId']")) \
            .select_by_visible_text("LAP")
        time.sleep(SHORT_WAIT)

        print("Selecting Scheme: LAP")
        Select(driver.find_element(By.CSS_SELECTOR, "select[formcontrolname='schemeId']")) \
            .select_by_visible_text("LAP")
        time.sleep(MEDIUM_WAIT)

        print("Selecting Purpose: Business Unit Development")
        Select(driver.find_element(By.CSS_SELECTOR, "select[formcontrolname='purposeEndUseId']")) \
            .select_by_visible_text("Business Unit Development")
        time.sleep(SHORT_WAIT)

        print("Entering remarks...")
        remarks_field = driver.find_element(By.CSS_SELECTOR, "textarea[formcontrolname='endUseRemarks']")

        remarks = (
            "The purpose of this loan is to support the development and enhancement of our existing business unit. "
            "The funds will be utilized for upgrading infrastructure, purchasing necessary equipment, "
            "improving operational efficiency, expanding production capacity, and addressing immediate "
            "working capital requirements to ensure smooth business operations and sustainable growth."
        )

        if len(remarks) < 100:
            remarks += " Additional details: This investment will help maintain quality standards and meet growing customer demand effectively."

        remarks_field.clear()
        remarks_field.send_keys(remarks)
        print(f"Remarks entered ({len(remarks)} characters)")
        time.sleep(MEDIUM_WAIT)

        print("Clicking Continue button...")
        driver.find_element( By.CSS_SELECTOR,"input[type='button'][value='Continue'].btn-orange").click()

        time.sleep(LONG_WAIT)

        print("\n" + "═" * 70)
        print("Continue button clicked – proceeding to next section")
        print("Current URL:", driver.current_url)
        print("Page title: ", driver.title)
        print("═" * 70)

        time.sleep(5)  # observe next screen

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