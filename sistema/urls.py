from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.defaults import page_not_found

not_found_exception = {'exception': Exception('Not Found')}

urlpatterns = [
    path('', include('progame.urls')),
    path('', include('ausers.urls')),

    path('admin/', admin.site.urls),

    # ckeditor
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # override allauth
    path("accounts/signup/", page_not_found, not_found_exception, name="account_signup"),
    path("accounts/login/", page_not_found, not_found_exception, name="account_login"),
    path("accounts/logout/", page_not_found, not_found_exception, name="account_logout"),

    # allauth
    path('accounts/', include('allauth.urls')),

    path('api/', include('api.urls')),

    # stats
    path('diagnostico/', include('stats.urls')),

    path('', include('quiz.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + staticfiles_urlpatterns()
