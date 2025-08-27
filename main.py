import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# --- 1. CONFIGURE THIS SECTION ---
USERNAME = ""
PASSWORD = ""
# A URL that detects captive portals
WIFI_CHECK_URL = "https://www.google.com"

# --- Selenium Script ---


def login_with_selenium():
    """
    Uses a headless Firefox browser to check for a captive portal
    and automates the WiFi login only if necessary.
    """
    print("Initializing headless browser...")
    options = Options()
    options.add_argument("--headless")

    # Set a page load timeout to prevent the script from hanging indefinitely
    options.page_load_strategy = 'eager'  # Doesn't wait for all images/stylesheets
    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(15)  # Set a 15-second timeout for page loads

    try:
        print(f"Navigating to captive portal check URL: {WIFI_CHECK_URL}")
        try:
            # This command may time out if we are already online due to the 204 response.
            # We can safely ignore this specific timeout.
            driver.get(WIFI_CHECK_URL)
        except TimeoutException:
            print(
                "Page load timed out, which is expected when already online. Checking URL...")
            pass

        # --- 2. Check if a Login is Required ---
        current_url = driver.current_url
        print(f"Current URL is: {current_url}")

        if "login.microsoftonline.com" in current_url:
            print("Redirected to login page. Authentication is required.")

            # --- 3. Interact with the Login Form ---
            wait = WebDriverWait(driver, 20)

            print("Entering email...")
            email_field = wait.until(
                EC.visibility_of_element_located((By.NAME, "loginfmt")))
            email_field.send_keys(USERNAME)
            driver.find_element(By.ID, "idSIButton9").click()

            print("Entering password...")
            password_field = wait.until(
                EC.visibility_of_element_located((By.NAME, "passwd")))
            password_field.send_keys(PASSWORD)
            driver.find_element(By.ID, "idSIButton9").click()

            print("Handling 'Stay signed in?' prompt...")
            stay_signed_in_no_button = wait.until(
                EC.element_to_be_clickable((By.ID, "idBtn_Back")))
            stay_signed_in_no_button.click()

            print("Login process complete!")
        else:
            print("Already connected to the internet. No login required. ✅")

    except Exception as e:
        print(f"An error occurred during the Selenium process: {e}")
        driver.save_screenshot("selenium_error.png")
        print("Saved a screenshot to selenium_error.png for debugging.")
        sys.exit(1)
    finally:
        driver.quit()


if __name__ == "__main__":
    login_with_selenium()
