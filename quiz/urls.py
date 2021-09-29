from django.urls import re_path, path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

app_name = 'quiz'

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + staticfiles_urlpatterns() + [

    path('quiz/<uuid:uuid>/links/', views.GetLinksAjuda.as_view(), name='get_links_ajuda'),
    path('quiz/<uuid:uuid>/link/adicionar/', views.LinkAjudaCreateView.as_view(), name='link_ajuda_create_view'),

    # react
    re_path(r'.*', views.index)

]