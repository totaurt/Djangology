from django.urls import path
from . import views

# urlpatterns = [
#     path('', views.post_list, name='post_list'),
# ]

urlpatterns = [
    # path('', views.character_list, name='character_list'),
    path('', views.post_list, name='post_list'),
    path('character/<str:id_character>/', views.character_detail, name='character_detail'),
    path('character/<str:id_character>/?<str:message>', views.character_detail, name='character_detail_mes'),
    # path('character/<int:pk>/', views.character_detail, name='character_detail'),
]