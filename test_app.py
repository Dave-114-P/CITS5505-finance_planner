"""Selenium test script for Finance Planner web application.
Please running the server by calling `python app.py` before executing this script.
This script automates the following test cases:
1. Home Page: Verify the title and navigation.
2. Registration: Test user registration with valid data.
3. Login: Test user login with valid credentials.
4. Share a Post: Test sharing a private post to anotheruser.
5. Upload a Spending Record: Test uploading a spending record.
6. Visualisation Page: Verify the presence of charts.
7. Profile Page: Verify the profile page.
8. Upload Income: Test uploading an income record.
9. Estimation Page: Test lifestyle selection and change.
10. View a Public Share & Add/Edit Comment: Test viewing a public share and adding/editing a comment if there's a public share."""

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Path to ChromeDriver for this session only
chrome_driver_path = "C:/drivers/chromedriver-win64/chromedriver.exe"
class FinancePlannerTest(unittest.TestCase):

    def setUp(self):
        # Launch Chrome browser and define base URL
        self.driver = webdriver.Chrome()
        self.base_url = "http://localhost:5000"

    def test_full_flow(self):
        driver = self.driver

        # ---------- Test 1: Home Page ----------
        driver.get(self.base_url)
        self.assertIn("Finance Planner", driver.page_source)
        time.sleep(1)

        # ---------- Test 2: Registration ----------
        driver.find_element(By.ID, "nav_register").click()
        time.sleep(1)
        driver.find_element(By.ID, "username").send_keys("testuser3")
        driver.find_element(By.ID, "email").send_keys("testuser3@example.com")
        driver.find_element(By.ID, "male").click()
        driver.find_element(By.ID, "password").send_keys("testpassword")
        driver.find_element(By.ID, "confirm_password").send_keys("testpassword")
        driver.find_element(By.NAME, "submit").click()
        time.sleep(2)

        driver.find_element(By.ID, "sign_up_here").click()
        time.sleep(1)
        driver.find_element(By.ID, "username").send_keys("anotheruser")
        driver.find_element(By.ID, "email").send_keys("anotheruser@example.com")
        driver.find_element(By.ID, "male").click()
        driver.find_element(By.ID, "password").send_keys("anothertestpassword")
        driver.find_element(By.ID, "confirm_password").send_keys("anothertestpassword")
        driver.find_element(By.NAME, "submit").click()
        time.sleep(2)

        # ---------- Test 3: Login ----------
        time.sleep(1)
        driver.find_element(By.ID, "username").send_keys("testuser3")
        driver.find_element(By.ID, "password").send_keys("testpassword")
        driver.find_element(By.NAME, "submit").click()
        time.sleep(2)
        # Optional check: skip if homepage doesn't show "Welcome"
        # self.assertIn("Welcome", driver.page_source)

        # ---------- Test 4: Share a Post ----------
        driver.find_element(By.ID, "nav_share").click()
        time.sleep(1)

        # Fill receiver (dummy username)
        driver.find_element(By.ID, "receiver-input").send_keys("anotheruser")
        time.sleep(1)

        # Select category
        driver.find_element(By.NAME, "category").send_keys(Keys.ARROW_DOWN)
        driver.find_element(By.NAME, "category").send_keys(Keys.RETURN)

        # Title and content
        driver.find_element(By.NAME, "title").send_keys("Test Share Title")
        driver.find_element(By.NAME, "content").send_keys("Test share content")

        # Scroll down to make the comment button visible
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Select first radio button for public/private
        time.sleep(2)
        radios = driver.find_elements(By.NAME, "is_public")
        # Check if the radio buttons were found
        if radios: #debug unable to click radio button
            # Click the radio button with value "off" (Private)
            for radio in radios:
                if radio.get_attribute("value") == "off":  # Replace "off" with "on" if you want Public
                    radio.click()
                    break
        else:
            raise Exception("No is_public radio buttons found")

        driver.find_element(By.NAME, "submit").click()
        time.sleep(2)

        # ---------- Test 5: Upload a Spending Record ----------
        driver.find_element(By.ID, "nav_transaction").click()
        time.sleep(1)
        driver.find_element(By.ID, "dropdownMenuButton").click()
        time.sleep(1)
        driver.find_element(By.ID, "add_spending").click()
        time.sleep(1)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "amount"))).send_keys("123.45")
        driver.find_element(By.NAME, "category").send_keys(Keys.ARROW_DOWN)
        driver.find_element(By.NAME, "category").send_keys(Keys.RETURN)
        driver.find_element(By.NAME, "date").send_keys("10-05-2025")
        driver.find_element(By.NAME, "description").send_keys("Test expense upload")
        driver.find_element(By.NAME, "submit").click()
        time.sleep(2)
         # ---------- Test 6: Visualisation Page ----------
        driver.find_element(By.ID, "nav_visualise").click()
        time.sleep(1)
        canvas_elements = driver.find_elements(By.TAG_NAME, "canvas")
        self.assertTrue(len(canvas_elements) > 0, "No charts found on /visualise page")
        # Scroll down to see the charts
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        # Scroll back up to the top
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

        # ---------- Test 7: Profile Page ----------
        driver.find_element(By.ID, "nav_user").click()
        time.sleep(1)
        driver.find_element(By.ID, "nav_profile").click()
        time.sleep(1)
        self.assertIn("Profile", driver.page_source)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        # Scroll back up to the top
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

        # ---------- Test 8: Upload Income ----------
        driver.find_element(By.ID, "nav_home").click()
        time.sleep(1)
        driver.find_element(By.ID, "upload_spending_from_home").click()
        time.sleep(1)
        driver.find_element(By.ID, "switch_income").click()
        time.sleep(1)

        driver.find_element(By.NAME, "amount").send_keys("888.88")
        driver.find_element(By.NAME, "category").send_keys(Keys.ARROW_DOWN)
        driver.find_element(By.NAME, "category").send_keys(Keys.RETURN)
        driver.find_element(By.NAME, "date").send_keys("14-05-2025")
        driver.find_element(By.NAME, "description").send_keys("Selenium income test")
        driver.find_element(By.NAME, "submit").click()
        time.sleep(2)

        # ---------- Test 9: Estimation Page (Choose or Change Lifestyle) ----------
        driver.find_element(By.ID, "nav_fee_estimation").click()
        time.sleep(1)

        # Case 1: First-time selection
        if driver.find_elements(By.NAME, "lifestyle"):
            driver.find_element(By.NAME, "lifestyle").send_keys(Keys.ARROW_DOWN)
            driver.find_element(By.NAME, "lifestyle").send_keys(Keys.RETURN)
            driver.find_element(By.CLASS_NAME, "action-button").click()
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
        else:
            # Case 2: Already selected → change it
            if driver.find_elements(By.CLASS_NAME, "action-button"):
                driver.find_element(By.CLASS_NAME, "action-button").click()
                time.sleep(1)
                driver.find_element(By.NAME, "lifestyle").send_keys(Keys.ARROW_DOWN)
                driver.find_element(By.NAME, "lifestyle").send_keys(Keys.RETURN)
                driver.find_element(By.CLASS_NAME, "action-button").click()
                time.sleep(1)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(1)

        # ---------- Test 10: View a Public Share & Add/Edit Comment ----------
        driver.find_element(By.ID, "nav_share").click()
        time.sleep(2)

        # Switch to "Public Shares" tab
        public_tab = driver.find_element(By.ID, "public-tab")
        public_tab.click()
        time.sleep(2)

        # Look for public posts
        view_buttons = driver.find_elements(By.LINK_TEXT, "View & Comment")
        if view_buttons:
            view_buttons[0].click()
            time.sleep(2)

            # Post a comment before editing
            comment_box = driver.find_element(By.ID, "new_comment_field")
            comment_box.send_keys("Comment to be edited")
            time.sleep(1)
            # Scroll down to make the comment button visible
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            driver.find_element(By.ID, "add_comment").click()
            time.sleep(2)

            # Find the "✏️ Edit" button
            edit_buttons = driver.find_elements(By.XPATH, "//button[contains(text(),'✏️ Edit')]")
            if edit_buttons:
                edit_buttons[0].click()
                time.sleep(1)

                # Fill modal
                edit_input = driver.find_element(By.ID, "editCommentContent")
                edit_input.clear()
                edit_input.send_keys("Edited via Selenium")

                driver.find_element(By.CSS_SELECTOR, "#editCommentForm button[type='submit']").click()
                time.sleep(2)
                self.assertIn("Edited via Selenium", driver.page_source)
            else:
                print("❗ No edit button found for this comment.")
        else:
            print("❗ No public posts found in share page.")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()