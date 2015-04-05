from django.contrib.staticfiles.testing import StaticLiveServerTestCase

# import unittest
# import time
from lists.models import Item

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
                (inputbox.location['x'] + inputbox.size['width'] / 2),
                512,
                delta=3
        )

        # She starts a new list and sees the input is nicely
        # centered there too
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
                inputbox.location['x'] + inputbox.size['width'] / 2,
                512,
                delta=3
        )

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Popei uses an online to-do app.
        # He opens the home page
        self.browser.get(self.live_server_url)

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

        # When he hits enter, he is taken to a new url,
        # now the page lists "1: Buy TDD book" as an item
        # in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_table('1: Buy TDD book')
        popei_list_url = self.browser.current_url
        self.assertRegex(popei_list_url, '/lists/.+')
        self.check_for_row_in_table('1: Buy TDD book')

        # He still needs to add other items to the to-do list
        # So he types 'Sleep tight', then he hits enter
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Sleep tight')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now the list contains the two items
        self.check_for_row_in_table('1: Buy TDD book')
        self.check_for_row_in_table('2: Sleep tight')

        # Now a new user, Brutus, comes along to the site
        self.browser.quit()
        Item.objects.all().delete()
        # We use a new browser session so that no information
        # from edith's session come throught
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)

        # Brutus visits the home page.
        # There is no sign of edith's list
        self.browser.get(self.live_server_url)
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy TDD book', body_text)
        self.assertNotIn('Sleep tight', body_text)

        # Brutus enters a new item into the empy list.
        # He is less interesting than Popei
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milch!?')
        inputbox.send_keys(Keys.ENTER)

        # Francis gets his own unique url
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, popei_list_url)

        # Again there is no trace of Popei's list
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy TDD book', body_text)
        self.assertIn('Buy milch!?', body_text)

        # satisfied, he goes to the gym
