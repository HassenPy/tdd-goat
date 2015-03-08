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
        self.fail('Finish the test!')

        # He wants to enter a to-do item as usual

        # He types "Buy TDD book" into a text box

        # When he hits enter, the page updates and now the page lists
        # "1: Buy TDD book" as an item in a to-do list

        # He still needs to add other items to the to-do list
        # He enters "Sleep tight"

        # The page updates again, and now the list contains the two items

        # He copies the url to access his to-do list anywhere he goes.

        # He visits that url later

        # He goes back to watever he was doing


if __name__ == '__main__':
    unittest.main(warnings='ignore')
