from django.urls import path

from authapp.views import update_hab
from habapp.views import IndexView, HabDetailView, \
    HabCreateView, HabUpdateView, HabDeleteView, like_hab, \
    CategoryHabView, HabListView, HabPublished


app_name = 'habapp'

urlpatterns = [
    # path('', IndexView.as_view(), name='main'),
    # path('index/', IndexView.as_view(), name='main'),
    path('new/', HabCreateView.as_view(), name='add'),
    path('list/', HabListView.as_view(), name='list'),
    path('<uuid:pk>/', HabDetailView.as_view(), name='detail'),
    path('<uuid:pk>/edit/', update_hab, name='edit'),
    path('<uuid:pk>/delete/', HabDeleteView.as_view(),
         name='delete'),
    path('<uuid:pk>/like/', like_hab, name='like-art'),
    path('category/<int:pk>', CategoryHabView.as_view(), name='hab_category'),
    path('<uuid:pk>/published/', HabPublished.as_view(), name='public'),
]
