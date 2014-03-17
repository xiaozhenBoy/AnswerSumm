from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'CQA.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^mycqa/','mycqa.views.index'),
    url(r'^index/$','mycqa.views.search'),
    url(r'^images/(?P<path>.*)$','django.views.static.serve',{'document_root':'/home/xuzhen/dijango/CQA/mycqa/templates/images'}),
   # url(r'^index/page=\d&query=(.*?)', 'mycqa.views.search'),
    url(r'^question/', 'mycqa.views.viewQuestion'),
    url(r'^admin/', include(admin.site.urls)),
)
