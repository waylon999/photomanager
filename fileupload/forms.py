from django.forms import ModelForm
from fileupload.models import Picture

class ImageForm(ModelForm):
    class Meta:
        model = Picture

