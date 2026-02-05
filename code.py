from concurrent.futures import wait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

GECKO_DRIVER_PATH = r"D:\RAJENDRAN\AUTOMATION\SELENIUM\geckodriver.exe"
BASE_URL = "https://uatngl.manappuram.com/lead/#/login"
CREDENTIALS = {
    "username": "369343",
    "password": "soft1234"
}

# Timeouts (in seconds)
SHORT_WAIT    = 2
MEDIUM_WAIT   = 4
LONG_WAIT     = 6
VERY_LONG_WAIT = 12
DROPDOWN_WAIT = 3

def main():
    service = Service(executable_path=GECKO_DRIVER_PATH)
    driver = webdriver.Firefox()
    driver.maximize_window()
    
    wait = WebDriverWait(driver, 15)  # reusable wait (increased to 15s for safety)
    
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
        login_button = driver.find_element(By.XPATH, "//button[contains(., 'Login') and contains(@class, 'btn-warning')]")
        login_button.click()
        print("Login button clicked → waiting for dashboard / next page...")
        time.sleep(LONG_WAIT)
        
        print("Clicking OK on popup...")
        driver.find_element(By.XPATH, "//button[contains(@class, 'ant-btn-primary')]//span[normalize-space(.)='OK']").click()
        time.sleep(MEDIUM_WAIT)
        print("OK clicked → waiting after popup close...")
        time.sleep(MEDIUM_WAIT)
        
        print("Clicking 'Create Lead' sidebar navigation link...")
        create_lead_link = driver.find_element(By.XPATH, "//app-sidebar-nav-link-content[.//i[contains(@class, 'cil-user-plus')]]//text()[normalize-space(.)='Create Lead']/ancestor::a")
        create_lead_link.click()
        print("'Create Lead' clicked → waiting for lead creation form...")
        time.sleep(SHORT_WAIT)
        
        print("Clicking Lead Type dropdown...")
        dropdown_control = driver.find_element(By.XPATH, "//nz-select[contains(@nzplaceholder, 'Select Lead Type')]//nz-select-top-control")
        dropdown_control.click()
        
        print("Waiting for 'New Lead' option to become visible...")
        new_lead_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class, 'ant-select-item-option-content') and normalize-space(.)='New Lead']")
            )
        )
        new_lead_option.click()
        print("'New Lead' selected successfully")
        time.sleep(1)  # small breath after selection
        
        print("Entering Applicant Name...")
        name_field = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@placeholder=\"Enter Applicant's Full Name\"]")
            )
        )
        name_field.clear()
        name_field.send_keys("Ragavan")
        time.sleep(SHORT_WAIT)
        
        print("Filling Mobile Numbers...")
        mobile_fields = wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//input[@placeholder=\"Enter Applicant's Mobile Number\"]")
            )
        )
        
        print(f"→ Found {len(mobile_fields)} mobile number field(s)")
        
        if len(mobile_fields) >= 2:
            # Mobile Number 1 (first field)
            mobile_fields[0].clear()
            mobile_fields[0].send_keys("8883961111")
            time.sleep(SHORT_WAIT)
            
            # Mobile Number 2 (second field)
            mobile_fields[1].clear()
            mobile_fields[1].send_keys("8883961111")
            time.sleep(SHORT_WAIT)
            
            print("Both Mobile 1 and Mobile 2 filled successfully")
        
        elif len(mobile_fields) == 1:
            print("WARNING: Only ONE mobile number field is visible right now")
            print("→ Filling it as Mobile 1 (check form if Mobile 2 should appear)")
            mobile_fields[0].clear()
            mobile_fields[0].send_keys("8883961111")
        
        else:
            print("ERROR: No mobile number fields detected!")
            driver.save_screenshot("mobile_fields_missing.png")
        
        print("Opening Lead Source dropdown...")
        # Use EXACT placeholder + structure from your HTML
        source_dropdown = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, 
                 "//nz-select[@nzplaceholder='Select the lead source']//nz-select-top-control"
                )
            )
        )    
        source_dropdown.click()
        time.sleep(1.2)  
        
        print("Waiting for 'Own lead' option to be present and clickable...")
        own_lead_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, 
                 "//nz-option-item[@title='Own lead' or .//div[contains(@class, 'ant-select-item-option-content') and normalize-space(.)='Own lead']]"
                )
            )
        )     
        driver.execute_script("arguments[0].scrollIntoView({block: 'nearest', inline: 'center'});", own_lead_option)
        time.sleep(0.5)
        driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));", own_lead_option)
        time.sleep(0.3)
        
        own_lead_option.click()
        print("'Own lead' selected successfully")
        time.sleep(1.5)  
        
        print("Entering Lead Generator Mobile Number...")
        lg_mobile_field = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@placeholder=\"Enter LG Mobile Number\"]")
            )
        )
        lg_mobile_field.clear()
        lg_mobile_field.send_keys("6543210989") 
        time.sleep(SHORT_WAIT)
        
        print("Lead Generator Mobile Number entered successfully")
        
        print("Opening Product Type dropdown...")
        
        # Locate using exact placeholder
        product_dropdown = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//nz-select[@nzplaceholder='Select product Type']//nz-select-top-control")
            )
        )
        
        product_dropdown.click()
        time.sleep(1.0)  # give time for options to load / animation
        
        print("Selecting 'LAP' option...")
        
        lap_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, 
                 "//div[contains(@class, 'ant-select-item-option-content') and normalize-space(.)='LAP']"
                )
            )
        )
        
        # Scroll if needed (helps with any hidden/virtual options)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", lap_option)
        time.sleep(0.4)
        
        lap_option.click()
        print("'LAP' selected successfully")
        time.sleep(1.2)  # allow form to update / validation to run
        print("Opening Loan Scheme dropdown...")
        
        # Locate using exact placeholder (most reliable here)
        scheme_dropdown = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//nz-select[@nzplaceholder='Select the loan scheme']//nz-select-top-control")
            )
        )
        
        # Alternative using label (if placeholder changes in future)
        # scheme_dropdown = wait.until(
        #     EC.element_to_be_clickable(
        #         (By.XPATH, "//label[contains(normalize-space(.), 'Scheme') or contains(normalize-space(.), 'Loan Scheme')]/following-sibling::div//nz-select-top-control")
        #     )
        # )
        
        scheme_dropdown.click()
        time.sleep(1.0)  # allow dropdown to open + options to render
        
        print("Selecting 'LAP' as Loan Scheme...")
        
        lap_scheme_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, 
                 "//div[contains(@class, 'ant-select-item-option-content') and normalize-space(.)='LAP']"
                )
            )
        )
        
        # Scroll into view (important if list is long or virtual-scrolled)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", lap_scheme_option)
        time.sleep(0.4)
        
        lap_scheme_option.click()
        print("'LAP' selected as Loan Scheme successfully")
        time.sleep(1.5)  # give time for dependent fields to load / form validation
        
        print("Entering Total Loan Amount Requested...")
        
        loan_amount_field = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@placeholder=\"Total Loan Amount Requested\"]")
            )
        )
        
        loan_amount_field.clear()
        loan_amount_field.send_keys("500000")  # ← change to the desired amount (e.g. 500000 for 5 lakhs)
        time.sleep(SHORT_WAIT)
        
        print("Loan Amount entered successfully")
        
        
        print("Entering PIN Code...")
        
        pincode_field = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@placeholder=\"PIN Code\"]")
            )
        )
        
        pincode_field.clear()
        pincode_field.send_keys("600001")  # ← change to a valid Chennai-area PIN code (example: 600001)
        time.sleep(SHORT_WAIT)
        
        print("PIN Code entered successfully")
        
        print("Opening State dropdown...")
        state_dropdown = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//nz-select[@nzplaceholder='Select State']//nz-select-top-control"
                )
            )
        )    
        state_dropdown.click()
        time.sleep(1.2)
        
        print("Typing 'Tamil Nadu' to filter...")
        # Find the search input inside the opened dropdown
        search_input = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//nz-select[@nzplaceholder='Select State']//input[contains(@class, 'ant-select-selection-search-input')]"
                )
            )
        )
        
        search_input.clear()
        search_input.send_keys("Tamil Nadu")
        time.sleep(1.5)   # wait for filtering / API response if any
        
        print("Waiting for 'Tamil Nadu' option to be present and clickable after search...")
        tamil_nadu_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//nz-option-item[@title='Tamil Nadu' or .//div[contains(@class, 'ant-select-item-option-content') and normalize-space(.)='Tamil Nadu']]"
                )
            )
        )
        
        driver.execute_script("arguments[0].scrollIntoView({block: 'nearest', inline: 'center'});", tamil_nadu_option)
        time.sleep(0.5)
        driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));", tamil_nadu_option)
        time.sleep(0.3)
        
        tamil_nadu_option.click()
        print("'Tamil Nadu' selected successfully")
        time.sleep(1.5)
        print("Opening Branch dropdown...")
        branch_dropdown = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//nz-select[@nzplaceholder='Select a branch']//nz-select-top-control"
                )
            )
        )    
        branch_dropdown.click()
        time.sleep(1.2)
        
        print("Typing 'KAMASHIPALAYAM' to filter...")
        # Locate the search input in the opened dropdown
        search_input = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//nz-select[@nzplaceholder='Select a branch']//input[contains(@class, 'ant-select-selection-search-input')]"
                )
            )
        )
        
        search_input.clear()
        search_input.send_keys("KAMASHIPALAYAM")
        time.sleep(1.5)  # wait for filtering (adjust if slow network/API)
        
        print("Waiting for 'KAMASHIPALAYAM (100)' option to be present and clickable...")
        branch_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//nz-option-item[@title='KAMASHIPALAYAM' or .//div[contains(@class, 'ant-select-item-option-content') and normalize-space(.)='KAMASHIPALAYAM (100)']]"
                )
            )
        )
        
        driver.execute_script("arguments[0].scrollIntoView({block: 'nearest', inline: 'center'});", branch_option)
        time.sleep(0.5)
        driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));", branch_option)
        time.sleep(0.3)
        
        branch_option.click()
        print("'KAMASHIPALAYAM (100)' selected successfully")
        time.sleep(1.5)
        
        print("Clicking 'Add Lead' button...")

        add_lead_button = wait.until(
        EC.element_to_be_clickable(
        (By.XPATH, "//button[@nztype='primary' and .//span[contains(., 'Add Lead')]]")))

        # Scroll (good practice)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_lead_button)
        time.sleep(0.4)   # ← reduced from 0.6 — usually enough

        # The magic line
        driver.execute_script("arguments[0].click();", add_lead_button)

        print("JS click executed on Add Lead button")
        time.sleep(1.2)   # ← give Angular time to open modal/form/new lead
        
        print("Current URL:", driver.current_url)
        print("Page title:", driver.title)
        
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