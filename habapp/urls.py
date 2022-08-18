from django.urls import path

from habapp.views import IndexView, HabDetailView, \
    HabCreateView, HabUpdateView, HabDeleteView, like_hab, \
    CategoryHabView, HabListView, HabPublished


app_name = 'habapp'

urlpatterns = [
    path('', IndexView.as_view(), name='main'),
    path('index/', IndexView.as_view(), name='main'),
    path('new/', HabCreateView.as_view(), name='add'),
    path('list/', HabListView.as_view(), name='list'),
    path('<uuid:pk>/', HabDetailView.as_view(), name='detail'),
    path('hab/<uuid:pk>/edit/', HabUpdateView.as_view(), name='edit'),
    path('hab/<uuid:pk>/delete/', HabDeleteView.as_view(),
         name='delete'),
    path('<uuid:pk>/like/', like_hab, name='like-hab'),
    path('category/<int:pk>', CategoryHabView.as_view(), name='hab_category'),
    path('<uuid:pk>/published/', HabPublished.as_view(), name='public'),
]
