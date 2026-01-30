"""
URL configuration for game app
"""
from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/start/', views.start_game, name='start_game'),
    path('api/level/', views.get_level, name='get_level'),
    path('api/recall/', views.get_recall_items, name='get_recall'),
    path('api/submit/', views.submit_answer, name='submit_answer'),
    path('api/next/', views.next_level, name='next_level'),
    path('api/results/', views.get_final_results, name='final_results'),
]
