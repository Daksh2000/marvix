from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_wikipedia, name='search_wikipedia'),
    path('save_article/', views.save_article, name='save_article'),
    path('saved_articles/', views.saved_articles, name='saved_articles'),
    path('edit_tags/<int:article_id>/', views.edit_tags, name='edit_tags'),
]
