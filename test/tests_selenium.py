import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

class SeleniumTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.wait = WebDriverWait(cls.driver, 60)  
        cls.base_url = "http://127.0.0.1:5000"  # Base URL of the website to test
        cls.register_and_login()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    @classmethod
    def register_and_login(cls):
        print("Starting registration process...")
        cls.driver.get(f"{cls.base_url}/register")
        
        try:
            username_input = cls.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            email_input = cls.driver.find_element(By.NAME, "email")
            password_input = cls.driver.find_element(By.NAME, "password")
            confirm_password_input = cls.driver.find_element(By.NAME, "confirm_password")
            submit_button = cls.driver.find_element(By.ID, "submit")

            unique_username = "new" + str(int(time.time()))
            unique_email = "new+" + str(int(time.time())) + "@gmail.com"

            username_input.send_keys(unique_username)
            email_input.send_keys(unique_email)
            password_input.send_keys("Test@us01")
            confirm_password_input.send_keys("Test@us01")

            print("Form filled, attempting to submit...")
            submit_button = cls.wait.until(EC.element_to_be_clickable((By.ID, "submit")))
            submit_button.click()

            print("Waiting for registration confirmation...")
            cls.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "alert-success"), "Your account has been created! You are now able to log in"))

            print("Registration successful, starting login process...")
            cls.driver.get(f"{cls.base_url}/login")
            email_input = cls.wait.until(EC.presence_of_element_located((By.NAME, "email")))
            password_input = cls.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            submit_button = cls.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and contains(text(), 'LOG IN NOW')]")))

            email_input.send_keys(unique_email)
            password_input.send_keys("Test@us01")

            print("Form filled, attempting to login...")
            submit_button.click()

            print("Waiting for home page...")
            cls.wait.until(EC.title_contains("Building community at UWA through books"))

            print("Login successful, home page loaded.")
        except Exception as e:
            print(f"Error during registration and login: {e}")

    def test_open_homepage(self):
        self.driver.get(self.base_url)
        self.assertIn('Building community at UWA through books', self.driver.page_source)

    def test_forum_page(self):
        self.driver.get(self.base_url)
        self.driver.find_element(By.LINK_TEXT, "Forum").click()
        self.wait.until(EC.title_contains("Forum"))
        self.assertIn("Forum", self.driver.title)
        posts = self.driver.find_elements(By.CLASS_NAME, "post-card")
        self.assertTrue(len(posts) > 0)

    def test_start_sharing_button(self):
        self.driver.get(self.base_url)
        start_sharing_btn = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "start-sharing-btn")))
        start_sharing_btn.click()
        self.wait.until(EC.url_contains("register"))
        self.assertIn("register", self.driver.current_url)

    def test_join_discussion_button(self):
        self.driver.get(self.base_url)
        join_discussion_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Join in Discussion')]")))
        self.driver.execute_script("arguments[0].scrollIntoView();", join_discussion_btn)
        self.wait.until(EC.element_to_be_clickable(join_discussion_btn))
        join_discussion_btn.click()
        self.wait.until(EC.url_contains("new_post"))
        self.assertIn("new_post", self.driver.current_url)

    def test_find_a_book_button(self):
        self.driver.get(self.base_url)
        find_book_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Find a Book')]")))
        self.driver.execute_script("arguments[0].scrollIntoView();", find_book_btn)
        self.wait.until(EC.element_to_be_clickable(find_book_btn))
        try:
            find_book_btn.click()
        except Exception as e:
            print(f"Error clicking Find a Book button: {e}")
            self.driver.execute_script("arguments[0].scrollIntoView();", find_book_btn)
            self.wait.until(EC.element_to_be_clickable(find_book_btn))
            find_book_btn.click()
        self.wait.until(EC.url_contains("shelf"))
        self.assertIn("shelf", self.driver.current_url)

    def test_customise_profile_button(self):
        self.driver.get(self.base_url)
        customise_profile_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Customise Profile')]")))
        self.driver.execute_script("arguments[0].scrollIntoView();", customise_profile_btn)
        self.wait.until(EC.element_to_be_clickable(customise_profile_btn))
        customise_profile_btn.click()
        self.wait.until(EC.url_contains("profile"))
        self.assertIn("profile", self.driver.current_url)

    def test_forum_join_buttons(self):
        self.driver.get(self.base_url)
        forum_join_buttons = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(),'Join')]")))
        for btn in forum_join_buttons:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView();", btn)
                self.wait.until(EC.element_to_be_clickable(btn))
                btn.click()
                self.wait.until(EC.url_contains("forum"))
                self.assertIn("forum", self.driver.current_url)
                self.driver.back()
                self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(),'Join')]")))
            except Exception as e:
                print(f"Error clicking Join button: {e}")
                self.driver.execute_script("arguments[0].scrollIntoView();", btn)
                self.wait.until(EC.element_to_be_clickable(btn))
                btn.click()
                self.wait.until(EC.url_contains("forum"))
                self.assertIn("forum", self.driver.current_url)
                self.driver.back()
                self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(),'Join')]")))

    def test_create_post(self):
        self.driver.get(self.base_url)
        self.driver.find_element(By.LINK_TEXT, "New Post").click()
        self.assertIn("New Post", self.driver.title)
        self.driver.find_element(By.NAME, "title").send_keys("Selenium Test Post")
        self.driver.find_element(By.NAME, "content").send_keys("This is a test post created by Selenium.")
        self.driver.find_element(By.NAME, "submit").click()
        self.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "alert-success"), "Your post has been created!"))

    def test_search_books(self):
        self.driver.get(self.base_url)
        self.driver.find_element(By.LINK_TEXT, "Book Shelf").click()
        search_box = self.wait.until(EC.presence_of_element_located((By.NAME, "query")))
        search_box.send_keys("Test Book")
        search_box.send_keys(Keys.RETURN)
        self.wait.until(EC.title_contains("Search Results"))
        results = self.driver.find_elements(By.CLASS_NAME, "book-card")
        self.assertTrue(len(results) > 0)

    def test_shelf_page(self):
        self.driver.get(self.base_url)
        self.driver.find_element(By.LINK_TEXT, "Book Shelf").click()
        self.wait.until(EC.title_contains("BookShelf"))
        books = self.driver.find_elements(By.CLASS_NAME, "col-cub")
        self.assertTrue(len(books) > 0)

    def test_update_profile(self):
        self.driver.get(self.base_url)
        self.driver.find_element(By.LINK_TEXT, "Profile").click()
        self.wait.until(EC.title_contains("Profile"))
        self.driver.find_element(By.NAME, "username").clear()
        self.driver.find_element
        (By.NAME, "username").send_keys("updateduser")
        self.driver.find_element(By.NAME, "email").clear()
        self.driver.find_element(By.NAME, "email").send_keys("updated@example.com")
        self.driver.find_element(By.NAME, "about_me").clear()
        self.driver.find_element(By.NAME, "about_me").send_keys("Updated about me")
        self.driver.find_element(By.NAME, "submit").click()
        self.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "alert-success"), "Your account has been updated!"))

    def test_add_comment(self):
        self.driver.get(self.base_url)
        self.driver.find_element(By.LINK_TEXT, "Forum").click()
        self.driver.find_element(By.CLASS_NAME, "title").click()
        self.assertIn("Post", self.driver.title)
        self.driver.find_element(By.NAME, "content").send_keys("This is a test comment.")
        self.driver.find_element(By.NAME, "submit").click()
        self.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "alert-success"), "Your comment has been created!"))

    def test_like_post(self):
        self.driver.get(self.base_url)
        self.driver.find_element(By.LINK_TEXT, "Forum").click()
        post_title = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
        self.driver.execute_script("arguments[0].scrollIntoView();", post_title)
        post_title.click()
        self.assertIn("Post", self.driver.title)
        like_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'btn-primary')]")))
        self.driver.execute_script("arguments[0].scrollIntoView();", like_button)
        self.wait.until(EC.element_to_be_clickable(like_button))
        like_button.click()
        self.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "alert-success"), "You liked the post!"))

    def test_follow_user(self):
        self.driver.get(self.base_url)
        self.driver.find_element(By.LINK_TEXT, "Forum").click()
        username_element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "username")))
        self.driver.execute_script("arguments[0].scrollIntoView();", username_element)
        username_element.click()
        self.wait.until(EC.title_contains("View User"))
        follow_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'btn-follow')]")))
        self.driver.execute_script("arguments[0].scrollIntoView();", follow_button)
        self.wait.until(EC.element_to_be_clickable(follow_button))
        follow_button.click()
        self.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "alert-success"), "You are now following"))

    def test_unfollow_user(self):
        self.driver.get(self.base_url)
        self.driver.find_element(By.LINK_TEXT, "Forum").click()
        username_element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "username")))
        self.driver.execute_script("arguments[0].scrollIntoView();", username_element)
        username_element.click()
        self.wait.until(EC.title_contains("View User"))
        unfollow_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'btn-unfollow')]")))
        self.driver.execute_script("arguments[0].scrollIntoView();", unfollow_button)
        self.wait.until(EC.element_to_be_clickable(unfollow_button))
        unfollow_button.click()
        self.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "alert-success"), "You are no longer following"))

    def test_update_post(self):
        self.driver.get(self.base_url)
        self.driver.find_element(By.LINK_TEXT, "Forum").click()
        post_title = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
        self.driver.execute_script("arguments[0].scrollIntoView();", post_title)
        post_title.click()
        update_button = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Update")))
        self.driver.execute_script("arguments[0].scrollIntoView();", update_button)
        update_button.click()
        self.wait.until(EC.title_contains("Update Post"))
        title_input = self.wait.until(EC.presence_of_element_located((By.NAME, "title")))
        title_input.clear()
        title_input.send_keys("Updated Selenium Test Post")
        content_input = self.driver.find_element(By.NAME, "content")
        content_input.clear()
        content_input.send_keys("This is the updated content.")
        submit_button = self.driver.find_element(By.NAME, "submit")
        self.driver.execute_script("arguments[0].scrollIntoView();", submit_button)
        submit_button.click()
        self.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "alert-success"), "Your post has been updated!"))

    def test_delete_post(self):
        self.driver.get(self.base_url)
        self.driver.find_element(By.LINK_TEXT, "Forum").click()
        post_title = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
        self.driver.execute_script("arguments[0].scrollIntoView();", post_title)
        post_title.click()
        delete_button = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "btn-danger")))
        self.driver.execute_script("arguments[0].scrollIntoView();", delete_button)
        delete_button.click()
        modal_delete_button = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "btn-post")))
        self.driver.execute_script("arguments[0].scrollIntoView();", modal_delete_button)
        self.wait.until(EC.element_to_be_clickable(modal_delete_button))
        modal_delete_button.click()
        self.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "alert-success"), "Your post has been deleted!"))

if __name__ == "__main__":
    unittest.main()







