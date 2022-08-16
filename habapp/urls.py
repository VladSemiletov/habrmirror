from django.urls import path

from authapp.views import update_hab
from habapp.views import IndexView, HabDetailView, \
    HabCreateView, HabUpdateView, HabDeleteView, like_hab, \
    CategoryHabView, HabListView, HabPublished


app_name = 'habapp'

urlpatterns = [
    path('', IndexView.as_view(), name='main'),
    path('index/', IndexView.as_view(), name='main'),
    path('hab/new/', HabCreateView.as_view(), name='add'),
    path('hab/list/', HabListView.as_view(), name='list'),
    path('hab/<uuid:pk>/', HabDetailView.as_view(), name='detail'),
    path('hab/<uuid:pk>/edit/', update_hab, name='edit'),
    path('hab/<uuid:pk>/delete/', HabDeleteView.as_view(),
         name='delete'),
    path('hab/<uuid:pk>/like/', like_hab, name='like-art'),
    path('hab/category/<int:pk>', CategoryHabView.as_view(), name='hab_category'),
    path('hab/<uuid:pk>/published/', HabPublished.as_view(), name='public'),
]
