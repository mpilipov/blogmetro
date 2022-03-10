from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
urlpatterns=[
    path('index', views.index, name='blog-main'),
    path('', views.home, name='blog-home'),
    path('contact', views.contact, name='blog-contact'),
    path('contact_thanks', views.contactthanks, name='blog-contactthanks'),
    path('search', views.search, name='blog-search'),
    path('search_results', views.search_results, name='blog-searchresult'),
    path('sign_in', views.signin, name='blog-signin'),
    path('sign_up', views.signup, name='blog-signup'),
    path('record/<slug:url_slug>', views.record, name='blog-record'),
    path('sign_out', LogoutView.as_view(), {'next_page':settings.LOGOUT_REDIRECT_URL }, name='blog-signout'),
    path('tag/<slug:slug>/', views.tag, name="blog-tag"),
]

