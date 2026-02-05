# lead_update.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

from utils import create_driver, perform_login
from config import CREDENTIALS


def update_lead():
    driver = create_driver()
    wait = WebDriverWait(driver, 15)

    try:
        creds = CREDENTIALS["sales_head"]

        # Use your exact login block
        perform_login(driver, creds["username"], creds["password"])

        print("Login should be successful now → proceeding to Lead Pool")

        # Click Lead Pool
        print("Clicking 'Lead Pool' sidebar link...")
        lead_pool_link = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@href, '#/lead/total-lead') or .//text()[contains(., 'Lead Pool')]]")
            )
        )
        driver.execute_script("arguments[0].click();", lead_pool_link)
        time.sleep(3.0)

        print("Lead Pool page should be open now.")

        lead_id = "L0100000775"
        print(f"Searching for Lead ID: {lead_id}")

        # Search input
        search_input = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@placeholder='Search Lead ID' or @name='search']")
            )
        )
        search_input.clear()
        search_input.send_keys(lead_id)
        time.sleep(2.0)

        # Verify lead exists
        lead_exists = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f"//td[contains(normalize-space(.), '{lead_id}')]")
            )
        )
        print(f"Success: Lead {lead_id} found in results")

        # Click to open lead details
        lead_cell = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//td[contains(normalize-space(.), '{lead_id}')]")
            )
        )
        driver.execute_script("arguments[0].click();", lead_cell)
        time.sleep(2.5)
        print("Lead detail page should be open now")

        # Click Call Status tab
        print("Clicking 'Call Status' tab...")
        call_status_tab = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//div[contains(@class, 'ant-tabs-tab') and .//div[contains(text(), 'Call Status')]]")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", call_status_tab)
        time.sleep(0.4)
        driver.execute_script("arguments[0].click();", call_status_tab)
        print("'Call Status' tab clicked")
        time.sleep(1.5)

        # Call Status dropdown → Interested
        print("Opening Call Status dropdown...")
        dropdown_control = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//nz-select[@nzplaceholder='Select calling status']//nz-select-top-control")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown_control)
        time.sleep(0.4)
        driver.execute_script("arguments[0].click();", dropdown_control)
        print("Dropdown opened → waiting for options...")
        time.sleep(1.2)

        print("Selecting 'Interested'...")
        interested_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//nz-option-item[.//div[contains(@class, 'ant-select-item-option-content') and normalize-space(.)='Interested']]")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'nearest', inline: 'center'});", interested_option)
        time.sleep(0.3)
        driver.execute_script("arguments[0].click();", interested_option)
        print("'Interested' selected successfully")
        time.sleep(1.5)

        # ── Sales Officer selection ────────────────────────────────────────
        print("Selecting Sales Officer from dropdown...")
        
        # Re-open Sales Officer dropdown (critical step)
        sales_dropdown = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//nz-select[contains(@nzplaceholder, 'Select Sales Officer')]//nz-select-top-control")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", sales_dropdown)
        time.sleep(0.4)
        driver.execute_script("arguments[0].click();", sales_dropdown)

        print("Sales Officer dropdown re-opened → waiting for search...")
        time.sleep(1.2)

        # Type in search input to filter
        search_input_officer = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//nz-select[contains(@nzplaceholder, 'Select Sales Officer')]"
                 "//input[contains(@class, 'ant-select-selection-search-input')]")
            )
        )
        search_input_officer.clear()
        search_input_officer.send_keys("369343")
        time.sleep(1.5)  # wait for filter

        # Click the option
        officer_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//nz-option-item[contains(@title, '369343') or "
                 ".//div[contains(@class, 'ant-select-item-option-content') and contains(., '369343')]]")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'nearest', inline: 'center'});", officer_option)
        time.sleep(0.3)
        driver.execute_script("arguments[0].click();", officer_option)

        print("'NIDHIN E A (369343)' selected successfully")
        time.sleep(1.5)

        # Update Call Status button
        print("Clicking 'Update Call Status' button...")
        update_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@nztype='primary' and .//span[contains(., 'Update Call Status')]]")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", update_button)
        time.sleep(0.4)
        driver.execute_script("arguments[0].click();", update_button)
        print("JS click executed on Update Call Status button")
        time.sleep(2.0)  # Give time for submission

    except Exception as e:
        print("Error:", str(e))
        timestamp = int(time.time())
        driver.save_screenshot(f"error_{timestamp}.png")
        print(f"Screenshot saved: error_{timestamp}.png")

    finally:
        driver.quit()
        print("Browser closed.")


if __name__ == "__main__":
    update_lead()