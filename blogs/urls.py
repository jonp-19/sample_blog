"""Defines URL patterns for blogs."""

from django.urls import path

from . import views

app_name = 'blogs'
urlpatterns = [
    # Home Page
    path('', views.index, name='index'),
    # Page for viewing posts
    path('entries/', views.entries, name='entries'),
    # Page for adding new post
    path('new_blogpost/', views.new_blogpost, name='new_blogpost'),
    # Page for editing post
    path('edit_blogpost/<int:blogpost_id>/', views.edit_blogpost, name='edit_blogpost'),
    ]