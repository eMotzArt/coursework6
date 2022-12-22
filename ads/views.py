from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from ads.models import Ad, Comment
from ads.serializers import AdvertisementsListSerializer, AdvertisementsRetrieveSerializer, CommentsListSerializer, CommentRetrieveSerializer
# Create your views here.

class AdvertisementsListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdvertisementsListSerializer

class AdvertisementRetrieveView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdvertisementsRetrieveSerializer


class AdvertisementsUserOwnerListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdvertisementsListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(author_id=request.user.id)
        return super().get(request, *args, **kwargs)


class CommentsListView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentsListSerializer

    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(ad=kwargs['pk'])
        return super().get(request, *args, **kwargs)

class CommentRetrieveView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentRetrieveSerializer
    lookup_field = 'id'
    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(ad_id=kwargs['ad_pk'], id=kwargs['id'])
        return super().get(request, *args, **kwargs)
