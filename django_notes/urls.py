from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path
from django.views.generic import RedirectView

from django_notes import views
from django_notes.views import EmailVerificationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notes/', include('notes.urls')),
    path('', RedirectView.as_view(url='/notes/', permanent=True)),
    path('accounts/', include('allauth.urls')),
    path('login/', views.UserLoginView.as_view(), name='notes_login'),
    path('logout/', LogoutView.as_view(), name='notes_logout'),
    path('register/', views.UserRegistrationView.as_view(), name='notes_register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('verify/<str:email>/<uuid:code>', EmailVerificationView.as_view(), name='email_verification'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
