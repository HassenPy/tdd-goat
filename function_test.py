import unittest
# import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(10)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Popei uses an online to-do app.
        # He opens the home page
        self.browser.get('http://127.0.0.1:8000')

        # He notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He wants to enter a to-do item as usual
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # He types "Buy TDD book" into a text box
        inputbox.send_keys("Buy TDD book")

        # When he hits enter, the page updates and now the page lists
        # "1: Buy TDD book" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_table('Buy TDD book')
        # He still needs to add other items to the to-do list
        # So he types 'Sleep tight', then he hits enter
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Sleep tight')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now the list contains the two items
        self.check_for_row_in_table('Buy TDD book')
        self.check_for_row_in_table('Sleep tight')

        # He copies the url to access his to-do list anywhere he goes.
        self.fail('Finish the test!')
        # He visits that url later

        # He goes back to whatever he was doing


if __name__ == '__main__':
    unittest.main(warnings='ignore')
