from fileupload.models import Picture
from fileupload.forms import ImageForm
from django.views.generic import CreateView, DeleteView

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.core.urlresolvers import reverse

from django.conf import settings

def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"


def upload_photo(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        import pdb; pdb.set_trace()
        if form.is_valid():
            saved = form.save()
            f = request.FILES.get('file')
            data = [{'name': f.name, 'url': settings.MEDIA_URL + "pictures/" + f.name.replace(" ", "_"), 'thumbnail_url': settings.MEDIA_URL + "pictures/" + f.name.replace(" ", "_"), 'delete_url': reverse('upload-delete', args=[saved.id]), 'delete_type': "DELETE"}]
            response = JSONResponse(data, {}, response_mimetype(request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            return response

    form = ImageForm()

    return render_to_response(
    'fileupload/picture_form.html', {'form': form},
    context_instance=RequestContext(request))


class PictureCreateView(CreateView):
    model = Picture

    def form_valid(self, form):
        import pdb; pdb.set_trace()
        self.object = form.save()
        f = self.request.FILES.get('file')
        data = [{'name': f.name, 'url': settings.MEDIA_URL + "pictures/" + f.name.replace(" ", "_"), 'thumbnail_url': settings.MEDIA_URL + "pictures/" + f.name.replace(" ", "_"), 'delete_url': reverse('upload-delete', args=[self.object.id]), 'delete_type': "DELETE"}]
        response = JSONResponse(data, {}, response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class PictureDeleteView(DeleteView):
    model = Picture

    def delete(self, request, *args, **kwargs):
        """
        This does not actually delete the file, only the database record.  But
        that is easy to implement.
        """
        self.object = self.get_object()
        self.object.delete()
        if request.is_ajax():
            response = JSONResponse(True, {}, response_mimetype(self.request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            return response
        else:
            return HttpResponseRedirect('/upload/new')

class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self,obj='',json_opts={},mimetype="application/json",*args,**kwargs):
        content = simplejson.dumps(obj,**json_opts)
        super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)
