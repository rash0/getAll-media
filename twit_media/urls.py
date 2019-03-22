from django.urls import re_path, path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    re_path(r'api/(?P<username>[\w-]+)/$', views.index, name='home'),
    re_path(r'home/', view = TemplateView.as_view(template_name='app.html')),
    # path(r'^user/$', views.index)
    # re_path(r'^user/$', views.scrap)

]
