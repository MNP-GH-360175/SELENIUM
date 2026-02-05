# utils.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from config import BASE_URL, SHORT_WAIT, MEDIUM_WAIT, LONG_WAIT

def create_driver():
    driver = webdriver.Firefox()
    driver.maximize_window()
    return driver

def perform_login(driver, username, password):
    # ── Your exact login code ────────────────────────────────────────
    print("Opening login page...")
    driver.get(BASE_URL)
    time.sleep(MEDIUM_WAIT)
    
    print("Entering username...")
    username_field = driver.find_element(By.NAME, "user")
    username_field.clear()
    username_field.send_keys(username)
    time.sleep(SHORT_WAIT)
    
    print("Entering password...")
    password_field = driver.find_element(By.NAME, "password")
    password_field.clear()
    password_field.send_keys(password)
    time.sleep(SHORT_WAIT)
    
    print("Clicking login button...")
    login_button = driver.find_element(
        By.XPATH,
        "//button[contains(., 'Login') and contains(@class, 'btn-warning')]"
    )
    login_button.click()
    print("Login button clicked → waiting for next page...")
    time.sleep(LONG_WAIT)
    
    # ── Popup after login ────────────────────────────────────────────
    print("Clicking OK on popup...")
    try:
        ok_button = driver.find_element(
            By.XPATH,
            "//button[contains(@class, 'ant-btn-primary')]//span[normalize-space(.)='OK']"
        )
        ok_button.click()
        time.sleep(MEDIUM_WAIT)
        print("OK clicked → waiting after popup...")
        time.sleep(MEDIUM_WAIT)
    except:
        print("   (Popup not found — continuing anyway)")