from django.conf.urls.defaults import *
from fileupload.views import PictureCreateView, PictureDeleteView

urlpatterns = patterns('fileupload.views',
    #(r'^new/$', PictureCreateView.as_view(), {}, 'upload-new'),
    (r'^delete/(?P<pk>\d+)$', PictureDeleteView.as_view(), {}, 'upload-delete'),
    (r'^one/$', 'upload_photo', {}, 'upload-new'),
)

