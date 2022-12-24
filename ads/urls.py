from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers
from ads import views
from ads.views import CommentsViewSet
# from ads.views import CommentsViewSet

# router = routers.SimpleRouter()
# router2 = routers.
# router.register(r'ads/(?P<pk>[^/.]+)/comments', CommentsViewSet, basename="comments")
urlpatterns = [
    path('ads/', views.AdvertisementsListView.as_view()),
    path('ads/me/', views.AdvertisementsUserOwnerListView.as_view()),
    path('ads/<pk>/', views.AdvertisementRetrieveView.as_view()),
    # path('ads/<pk>/comments/', views.CommentCreateView.as_view()),
    # path('ads/<pk>/comments/', views.CommentsListView.as_view()),
    path('ads/<pk>/comments/', views.CommentsViewSet.as_view({'get': 'list'})),
    path('ads/<ad_pk>/comments/<id>/', views.CommentRetrieveView.as_view()),
]

# urlpatterns+=router.urls
x=1

