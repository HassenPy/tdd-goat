from django.test import TestCase
from django.http import HttpRequest
from django.core.urlresolvers import resolve
from django.template.loader import render_to_string

# import time

from lists.views import home_page  # , new_list
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
        list_id = Item.objects.all()[0].list.id

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'],
                         '/lists/%d/' % (list_id,)
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
        list_ = List()
        list_.save()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_list_items(self):
        list_ = List()
        list_.save()

        Item.objects.create(text='itemey1', list=list_)
        Item.objects.create(text='itemey2', list=list_)

        response = self.client.get('/lists/%d/' % (list_.id,))

        self.assertEqual(Item.objects.all()[0].list, list_)
        self.assertContains(response, 'itemey1')
        self.assertContains(response, 'itemey2')


class NewListTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text="item1", list=correct_list)
        Item.objects.create(text="item2", list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text="item3", list=other_list)
        Item.objects.create(text="item4", list=other_list)

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')
        self.assertNotContains(response, 'item3')
        self.assertNotContains(response, 'item4')

    def test_redirects_after_POST(self):
        response = self.client.post(
                                    '/lists/new/',
                                    data={'item_text': 'A new list apart :D'}
                                )
        new_list_ = List.objects.all()[0]
        self.assertRedirects(response, '/lists/%d/' % (new_list_.id,))


class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post(
                '/lists/%d/new_item/' % (correct_list.id,),
                data={'item_text': 'A new item for an existing list'}
            )
        self.assertEqual(Item.objects.all().count(), 1)

        new_item = Item.objects.all()[0]
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post(
            '/lists/%d/new_item/' % (correct_list.id,),
            data={'item_text': 'A new item for an existing list'}
            )
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)
