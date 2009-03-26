from django.conf.urls.defaults import *
import weathercal.views

urlpatterns = patterns('',
    (r'^(?P<location>[0123456789]{5})/$', weathercal.views.for_zip),
)
