from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from homepage.views import login_view

urlpatterns = [
    path('homepage/', include("homepage.urls")),
    path('', include("homepage.urls")),
    # path('web/', include("homepage.urls")),
    path('admin/', admin.site.urls),
    path('login/', login_view, name="login_view"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
