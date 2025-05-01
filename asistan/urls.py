from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'asistan'  # Uygulama adı tanımlandı
urlpatterns = [
    path("process/", views.process, name="process"),
    path("process2/", views.process2, name="process2"),
    path("agents/", views.agents, name="agents"),
    path("agents_game/", views.agents_game, name="agents_game"),
    path("agents_process/", views.agents_process, name="agents_process"),
    path("agents_detail/<int:agents_id>/", views.agents_detail, name="agents_detail"),
    path("agents_payment/<int:agents_id>/", views.agents_payment, name="agents_payment"),
    path("instagram/", views.instagram, name="instagram"),
    path("x_twitter/", views.x_twitter, name="x_twitter"),
    path("yotube/", views.yotube, name="yotube"),
    path("yotube_shorts/", views.yotube_shorts, name="yotube_shorts"),
    path("whatsapp_business/", views.whatsapp_business, name="whatsapp_business"),

    path("instagram_agents_start/", views.instagram_agents_start, name="instagram_agents_start"),
    path("apps/", views.apps, name="apps"),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
