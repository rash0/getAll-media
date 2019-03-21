from django.urls import re_path, path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # path(r'^$', views.index, name='home'),
    # re_path(r'^$', views.index, name='index'),
    re_path(r'^$', view = TemplateView.as_view(template_name='app.html')),
    re_path(r'^user/(?P<username>[\w-]+)/$', views.index)
    # re_path(r'^user/$', views.scrap)

]
