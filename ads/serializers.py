from rest_framework import serializers
from ads.models import Ad, Comment


class AdvertisementsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['pk', 'image', 'title', 'price', 'description']

class AdvertisementsRetrieveSerializer(serializers.ModelSerializer):
    author_first_name = serializers.SerializerMethodField()
    author_last_name = serializers.SerializerMethodField()
    author_pk = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = ['pk', 'image', 'title', 'price', 'description', 'author_first_name', 'author_last_name', 'author_pk']

    def get_author_first_name(self, obj):
        return obj.author.first_name

    def get_author_last_name(self, obj):
        return obj.author.last_name

    def get_author_pk(self, obj):
        return obj.author.pk


class CommentsListSerializer(serializers.ModelSerializer):
    author_first_name = serializers.SerializerMethodField()
    author_last_name = serializers.SerializerMethodField()
    author_image = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['pk', 'text', 'author_id', 'created_at', 'author_first_name', 'author_last_name', 'ad_id', 'author_image']

    def get_author_first_name(self, obj):
        return obj.author.first_name

    def get_author_last_name(self, obj):
        return obj.author.last_name

    def get_author_image(self, obj):
        return obj.author.image.url or None

class CommentRetrieveSerializer(serializers.ModelSerializer):
    author_first_name = serializers.SerializerMethodField()
    author_last_name = serializers.SerializerMethodField()
    # author_image = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['pk', 'text', 'author_id', 'created_at', 'author_first_name', 'author_last_name', 'ad_id']#, 'author_image']

    def get_author_first_name(self, obj):
        return obj.author.first_name

    def get_author_last_name(self, obj):
        return obj.author.last_name

    # def get_author_image(self, obj):
    #     return obj.author.image or None


class CommentCreateSerializer(serializers.ModelSerializer):
    author_first_name = serializers.CharField(read_only=True, required=False, max_length=150)
    author_last_name = serializers.CharField(read_only=True, required=False, max_length=150)
    # author_image = serializers.ImageField()
    # ad_id = serializers.SerializerMethodField()
    author_id = serializers.IntegerField(required=False)

    class Meta:
        model = Comment
        fields = ['pk', 'text', 'author_id', 'created_at', 'author_first_name', 'author_last_name', 'ad_id']#, 'author_image']

    def create(self, validated_data):
        validated_data['ad_id'] = self.initial_data['current_ad'].id
        validated_data['author_id'] = self.initial_data['current_ad'].author_id
        validated_data['author_first_name'] = self.initial_data['current_ad'].author.first_name
        validated_data['author_last_name'] = self.initial_data['current_ad'].author.last_name
        return super().create(validated_data)

    # def get_ad_id(self, obj):
    #     x=1
    #     return 1

    # def get_author_first_name(self, obj):
        # return self.initial_data['author_first_name']
    #
    # def get_author_last_name(self, obj):
    #     return self.initial_data['author_last_name']

    # def get_author_image(self, obj):
    #     return self.initial_data['image'].url or None
