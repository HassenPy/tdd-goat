from django.test import TestCase
from django.http import HttpRequest
from django.core.urlresolvers import resolve
from django.template.loader import render_to_string

# import time

from lists.views import home_page, new_list
from lists.models import Item, List


class HomePageTest(TestCase):
    def test_root_url_resolvers_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_and_return_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_can_save_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.all().count(), 0)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = "A new list item"

        home_page(request)

        items_list = Item.objects.all()
        self.assertEqual(items_list.count(), 1)
        self.assertIn(request.POST['item_text'],
                      [item.text for item in items_list]
                      )

    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = "A new list item"
        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'],
                         '/lists/the-only-list/'
                         )


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = "The first(ever) list item"
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "The second item"
        second_item.list = list_
        second_item.save()

        saved_lists = List.objects.all()
        saved_items = Item.objects.all()

        self.assertEqual(saved_lists.count(), 1)
        self.assertEqual(saved_lists[0], list_)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, 'The first(ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'The second item')
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_list_items(self):
        list_ = List()
        list_.save()

        Item.objects.create(text='itemey1', list=list_)
        Item.objects.create(text='itemey2', list=list_)

        response = self.client.get('/lists/the-only-list/')

        self.assertEqual(Item.objects.all()[0].list, list_)
        self.assertContains(response, 'itemey1')
        self.assertContains(response, 'itemey2')


class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'
        new_list(request)

        self.assertEqual(Item.objects.all().count(), 1)

        new_item = Item.objects.all()[0]
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'
        response = new_list(request)

        self.assertEqual(response['location'], '/lists/the-only-list/')
        self.assertEqual(response.status_code, 302)

        # Writing tests for unique url
