from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

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
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertEqual(
            any(row.text == '1: Buy TDD book' for row in rows)
            )

        # He still needs to add other items to the to-do list
        # So he enters 'Sleep tight'
        self.fail('Finish the test!')

        # The page updates again, and now the list contains the two items

        # He copies the url to access his to-do list anywhere he goes.

        # He visits that url later

        # He goes back to watever he was doing


if __name__ == '__main__':
    unittest.main(warnings='ignore')
