# customer_details.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

from utils import create_driver, perform_login
from config import CREDENTIALS, SHORT_WAIT, MEDIUM_WAIT, LONG_WAIT


def enter_customer_details(lead_id):
    driver = create_driver()
    wait = WebDriverWait(driver, 20)  # Higher timeout for calendar stability

    try:
        creds = CREDENTIALS["sales_officer"]

        # Login
        perform_login(driver, creds["username"], creds["password"])
        print("Login successful → proceeding to Lead Pool")

        # Lead Pool navigation
        print("Clicking 'Lead Pool' sidebar link...")
        lead_pool_link = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@href, '#/lead/total-lead') or .//text()[contains(., 'Lead Pool')]]")
            )
        )
        driver.execute_script("arguments[0].click();", lead_pool_link)
        time.sleep(3.0)

        # Search & open lead
        print(f"Searching for Lead ID: {lead_id}")
        search_input = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@placeholder='Search Lead ID' or @name='search']")
            )
        )
        search_input.clear()
        search_input.send_keys(lead_id)
        time.sleep(2.5)

        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f"//td[contains(normalize-space(.), '{lead_id}')]")
            )
        )
        print(f"Success: Lead {lead_id} found")

        print("Opening lead details...")
        lead_cell = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//td[contains(normalize-space(.), '{lead_id}')]")
            )
        )
        driver.execute_script("arguments[0].click();", lead_cell)
        time.sleep(3.0)

        # Bureau Check tab
        print("Clicking 'Bureau Check' tab...")
        bureau_tab = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class, 'ant-tabs-tab') and .//div[contains(text(), 'Bureau Check')]]")
            )
        )
        driver.execute_script("arguments[0].click();", bureau_tab)
        time.sleep(2.0)

        # Add Applicant (normal, not OCR)
        print("Clicking normal 'Add Applicant' button...")
        add_applicant_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//button[@nzshape='round' and .//span[normalize-space(.)='Add Applicant']]"
                 "[not(contains(., 'OCR')) and not(contains(., 'By OCR'))]"
                )
            )
        )
        driver.execute_script("arguments[0].click();", add_applicant_button)
        time.sleep(3.5)  # Modal open delay

        # Applicant Type
        print("Setting Applicant Type...")
        applicant_type_value = "Applicant"  # Change to "Co-Applicant" for second+
        applicant_dropdown = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//nz-select[contains(@nzplaceholder, 'Select the applicant state') or "
                 "contains(@nzplaceholder, 'Applicant Type')]"
                 "//nz-select-top-control")
            )
        )
        driver.execute_script("arguments[0].click();", applicant_dropdown)
        time.sleep(1.2)

        search_input = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//nz-select[contains(@nzplaceholder, 'Select the applicant state') or "
                 "contains(@nzplaceholder, 'Applicant Type')]"
                 "//input[contains(@class, 'ant-select-selection-search-input')]")
            )
        )
        search_input.clear()
        search_input.send_keys(applicant_type_value)
        time.sleep(1.2)

        option_xpath = (
            f"//nz-option-item[contains(@title, '{applicant_type_value}') or "
            f".//div[contains(@class, 'ant-select-item-option-content') and normalize-space(.)='{applicant_type_value}']]"
        )
        applicant_option = wait.until(
            EC.element_to_be_clickable((By.XPATH, option_xpath))
        )
        driver.execute_script("arguments[0].click();", applicant_option)
        time.sleep(1.2)

        # Names
        print("Filling Applicant First Name and Last Name...")
        first_name_field = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@placeholder=\"Enter Applicant's First Name\"]")
            )
        )
        first_name_field.clear()
        first_name_field.send_keys("Rajendran")
        time.sleep(0.5)
        print("First Name entered")

        last_name_field = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@placeholder=\"Enter Applicant's Last Name\"]")
            )
        )
        last_name_field.clear()
        last_name_field.send_keys("N")
        time.sleep(0.5)
        print("Last Name entered")

        # Gender selection - Multiple fallback methods
        print("Selecting Gender: Male...")
        try:
            # Method 1: Try clicking the radio button directly
            male_radio = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//label[contains(@class, 'ant-radio-wrapper') and .//span[text()='Male']]")
                )
            )
            driver.execute_script("arguments[0].click();", male_radio)
            print("Gender selected: Male (Method 1)")
        except:
            try:
                # Method 2: Click the input inside the label
                male_radio_input = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//label[.//span[text()='Male']]//input[@type='radio']")
                    )
                )
                driver.execute_script("arguments[0].click();", male_radio_input)
                print("Gender selected: Male (Method 2)")
            except:
                # Method 3: Click the span element containing the radio
                male_span = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//span[@class='ant-radio' and following-sibling::span[text()='Male']]")
                    )
                )
                driver.execute_script("arguments[0].click();", male_span)
                print("Gender selected: Male (Method 3)")
        
        time.sleep(0.5)
# Date of Birth selection - Alternative method using direct input
        print("Selecting Date of Birth: 10-Aug-1997...")
        
        # Click the date picker to open calendar
        dob_picker = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//nz-date-picker[@nzformat='dd-MMM-yyyy']//input[@placeholder='Select date']")
            )
        )
        
        # Try direct input first (some date pickers accept direct text input)
        try:
            dob_picker.clear()
            dob_picker.send_keys("10-Aug-1997")
            time.sleep(1.0)
            print("Date entered directly: 10-Aug-1997")
        except:
            print("Direct input failed, using calendar method...")
            
            # Click to open calendar
            driver.execute_script("arguments[0].click();", dob_picker)
            time.sleep(2.0)
            
            # Wait for overlay to appear
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'cdk-overlay-pane')]")
                )
            )
            time.sleep(1.0)
            
            # Find and click the header button (year-month display)
            header_buttons = driver.find_elements(By.XPATH, 
                "//div[contains(@class, 'ant-picker-header')]//button"
            )
            
            if len(header_buttons) > 0:
                # Click the main header button (usually the first or middle one that shows year/month)
                for btn in header_buttons:
                    if '2026' in btn.text or 'Feb' in btn.text or btn.text.strip():
                        driver.execute_script("arguments[0].click();", btn)
                        time.sleep(1.0)
                        break
            
            # Click header again for year view
            header_buttons = driver.find_elements(By.XPATH, 
                "//div[contains(@class, 'ant-picker-header')]//button"
            )
            if len(header_buttons) > 0:
                for btn in header_buttons:
                    if btn.text.strip():
                        driver.execute_script("arguments[0].click();", btn)
                        time.sleep(1.0)
                        break
            
            # Navigate backwards using super-prev button
            print("Navigating to 1990s...")
            for i in range(3):
                try:
                    super_prev = driver.find_element(By.XPATH,
                        "//button[contains(@class, 'ant-picker-header-super-prev-btn') or contains(@class, 'prev')]"
                    )
                    driver.execute_script("arguments[0].click();", super_prev)
                    time.sleep(0.8)
                except:
                    pass
            
            # Click year 1997
            print("Selecting year 1997...")
            all_cells = driver.find_elements(By.XPATH,
                "//div[contains(@class, 'ant-picker-cell')]//div[contains(@class, 'ant-picker-cell-inner')]"
            )
            for cell in all_cells:
                if cell.text == '1997':
                    driver.execute_script("arguments[0].click();", cell)
                    time.sleep(1.0)
                    break
            
            # Click month Aug
            print("Selecting August...")
            all_cells = driver.find_elements(By.XPATH,
                "//div[contains(@class, 'ant-picker-cell')]//div[contains(@class, 'ant-picker-cell-inner')]"
            )
            for cell in all_cells:
                if cell.text == 'Aug':
                    driver.execute_script("arguments[0].click();", cell)
                    time.sleep(1.0)
                    break
            
            # Click day 10
            print("Selecting day 10...")
            all_cells = driver.find_elements(By.XPATH,
                "//div[contains(@class, 'ant-picker-cell') and not(contains(@class, 'disabled'))]//div[contains(@class, 'ant-picker-cell-inner')]"
            )
            for cell in all_cells:
                if cell.text == '10':
                    driver.execute_script("arguments[0].click();", cell)
                    time.sleep(1.0)
                    break
            
            print("Date of Birth selected: 10-Aug-1997")
# Address field
        print("Filling Address...")
        address_field = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@placeholder='Applicant Address' and @maxlength='50']")
            )
        )
        address_field.clear()
        address_field.send_keys("123 Main Street,23 Main Street,23 Main Street,23 Main Street,23 Main Street,23 Main Street,23 Main Street,23 Main Street")  # Replace with your address
        time.sleep(0.5)
        print("Address entered")
        
        # Address Category - Select "Permanent Address"
        print("Selecting Address Category: Permanent Address...")
        address_category_dropdown = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, 
                 "//label[text()='Address Category']/parent::div/following-sibling::div//nz-select//nz-select-top-control"
                )
            )
        )
        driver.execute_script("arguments[0].click();", address_category_dropdown)
        time.sleep(1.0)
        
        # Select "Permanent Address" option
        permanent_address_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, 
                 "//nz-option-item[contains(@title, 'Permanent Address') or "
                 ".//div[contains(@class, 'ant-select-item-option-content') and normalize-space(.)='Permanent Address']]"
                )
            )
        )
        driver.execute_script("arguments[0].click();", permanent_address_option)
        time.sleep(0.8)
        print("Address Category selected: Permanent Address")
        
        # PIN Code field
        print("Filling PIN Code...")
        pin_code_field = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@placeholder='PIN Code' and @type='number']")
            )
        )
        pin_code_field.clear()
        pin_code_field.send_keys("638314")
        time.sleep(0.5)
        print("PIN Code entered: 638314")
        # State dropdown - Select "Tamil Nadu"
        print("Selecting State: Tamil Nadu...")
        state_dropdown = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, 
                 "//label[text()='State']/parent::div/following-sibling::div//nz-select//nz-select-top-control"
                )
            )
        )
        driver.execute_script("arguments[0].click();", state_dropdown)
        time.sleep(1.2)
        print("State dropdown opened")
        
        # Type "Tamil Nadu" in the search input (since nzshowsearch is enabled)
        state_search_input = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, 
                 "//label[text()='State']/parent::div/following-sibling::div//nz-select//input[contains(@class, 'ant-select-selection-search-input')]"
                )
            )
        )
        state_search_input.clear()
        state_search_input.send_keys("Tamil Nadu")
        time.sleep(1.2)
        print("Typed 'Tamil Nadu' in search")
        
        # Select "Tamil Nadu" from the filtered options
        tamil_nadu_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, 
                 "//nz-option-item[contains(@title, 'Tamil Nadu') or "
                 ".//div[contains(@class, 'ant-select-item-option-content') and contains(., 'Tamil Nadu')]]"
                )
            )
        )
        driver.execute_script("arguments[0].click();", tamil_nadu_option)
        time.sleep(0.8)
        print("State selected: Tamil Nadu")
        # Mobile Number field
        print("Filling Mobile Number...")
        mobile_number_field = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@placeholder='Mobile Number' and @type='number']")
            )
        )
        mobile_number_field.clear()
        mobile_number_field.send_keys("8883961115")
        time.sleep(0.5)
        print("Mobile Number entered: 8883961115")
        # Click OK
       # Click OK button to submit the form
        print("Clicking OK button to submit form...")
        ok_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'ant-btn-primary')]//span[text()=' OK ']")
            )
        )
        driver.execute_script("arguments[0].click();", ok_button)
        time.sleep(2.5)
        print("Form submitted successfully!")

    except Exception as e:
        print("Error during customer details flow:", str(e))
        timestamp = int(time.time())
        driver.save_screenshot(f"customer_error_{timestamp}.png")
        print(f"Screenshot saved: customer_error_{timestamp}.png")

    finally:
        driver.quit()
        print("Browser closed.")


if __name__ == "__main__":
    test_lead_id = "L0100000775"  
    enter_customer_details(test_lead_id)