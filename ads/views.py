from rest_framework import viewsets
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ads.models import Ad, Comment
from ads.serializers import AdvertisementsListSerializer, AdvertisementsRetrieveSerializer, CommentsListSerializer, \
    CommentRetrieveSerializer, CommentCreateSerializer
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

class CommentCreateView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CommentsViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        queryset = Comment.objects.all().filter(ad=kwargs['pk'])
        serializer = CommentsListSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request.data['ad_id'] = kwargs['pk']
        request.data['author_id'] = request.user.id
        request.data['author_first_name'] = request.user.first_name
        request.data['author_last_name'] = request.user.last_name
        request.data['image'] = request.user.image



        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)