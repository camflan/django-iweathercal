from django.conf.urls.defaults import *
import iweathercal.views

urlpatterns = patterns('',
    (r'^(?P<location>\w{5,10})/$', iweathercal.views.for_zip),
)
