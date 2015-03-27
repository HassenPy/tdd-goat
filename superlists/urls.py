from django.conf.urls import patterns, url  # ,include
# from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'lists.views.home_page', name='home'),
    url(r'^lists/the-only-list/$', 'lists.views.view_list',
        name='view_list'
        ),
    url(r'^lists/new/$', 'lists.views.new_list', name='new_list'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^admin/', include(admin.site.urls)),
)
