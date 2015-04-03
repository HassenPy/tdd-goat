from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^(?P<list_id>(\d+))/$',
        'lists.views.display_list',
        name='display_list'
        ),
    url(r'^(?P<list_id>(\d+))/new_item/$',
        'lists.views.add_item',
        name='add_item'
        ),
    url(r'^(?P<list_id>(\d+))/$', 'lists.views.view_list',
        name='view_list'
        ),
    url(r'^new/$', 'lists.views.new_list', name='new_list'),
)
