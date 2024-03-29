
from django.conf.urls.defaults import patterns, include, handler500
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

handler500 = 'testproject.testapp.views.error'

urlpatterns = patterns(
    '',
    (r'^$', 'testproject.testapp.views.index'),
    (r'^error$', 'testproject.testapp.views.gen_error'),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
