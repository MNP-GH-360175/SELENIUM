from utils import create_driver, login, handle_popup
from config import CREDENTIALS, SHORT_WAIT

def sanction_lead(lead_id):
    driver = create_driver()
    wait = WebDriverWait(driver, 15)
    
    try:
        creds = CREDENTIALS["branch_manager"]
        login(driver, creds["username"], creds["password"])
        handle_popup(driver)
        
        # Navigate to leads for approval
        # ...
        
        # Sanction/Approve
        print("Sanctioning the lead...")
        sanction_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Sanction') or contains(., 'Approve')]")))
        driver.execute_script("arguments[0].click();", sanction_button)
        time.sleep(1.5)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    sanction_lead("example_lead_id")