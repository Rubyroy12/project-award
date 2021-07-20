from django.conf.urls import url
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.home,name = 'index'),
    path('profile/<str:username>/',views.profile,name='profile'),
    path('edit/profile/',views.update_profile,name='update'),
    path('^submitproject/$', views.submit,name='submit'),
    path('project/<id>/', views.project,name='project'),
    path(r'^ratings/', include('star_ratings.urls', namespace='ratings')),
    path('search/', views.search_project, name='search'),
    path('^api/profile/merch/$',views.MerchProfileList.as_view()),
    path('^api/project/merch/$',views.MerchProjectList.as_view())


]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)