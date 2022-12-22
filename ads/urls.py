from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from ads import views

urlpatterns = [
    path('ads/', views.AdvertisementsListView.as_view()),
    path('ads/me/', views.AdvertisementsUserOwnerListView.as_view()),
    path('ads/<pk>/', views.AdvertisementRetrieveView.as_view()),
    path('ads/<pk>/comments/', views.CommentCreateView.as_view()),
    path('ads/<pk>/comments/', views.CommentsListView.as_view()),
    path('ads/<ad_pk>/comments/<id>/', views.CommentRetrieveView.as_view()),
]
