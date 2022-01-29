from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from . import models


class LocationSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        build = attrs.get('building', '')
        build2 = attrs.get('address', '')
        if build == "saadaaa":
            raise serializers.ValidationError({"phoe": build + " is not correct"})
        elif build2 == "saaa":
            raise serializers.ValidationError({"qs": "number not correct"})

        return attrs

    class Meta:
        model = models.Location
        # fields='__all__'
        fields = ['id', 'building', 'address', 'location']


class UserCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Exist
        fields = ['id', 'email', 'phone']


class UserListOnClickSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    class Meta:
        model = models.Profile
        fields = ['id', 'name', 'surname', 'phone', 'address', 'ts', 'location_id', 'uid_id', 'email']

    def get_email(self, obj):
        try:
            a = models.User.objects.get(id=obj.uid_id)
            return a.email
        except:
            return None


class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = ['id', 'name', 'surname', 'phone', 'address', 'ts', 'location_id', 'uid_id']


class MeetingQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Meeting_Questions
        fields = ['id', 'meeting', 'question']


class DelegateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Daligate
        fields = ['id', 'meeting_id', 'user', 'delegated_to', 'delegated_sts', 'sts']

        def create(self, validated_data):
            return models.Daligate.objects.create(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = ['id', 'name', 'surname', 'phone', 'address', 'ts', 'location_id', 'uid']


class UserSignUpSerializer(serializers.ModelSerializer):
    vote_user = UserProfileSerializer(many=True)

    class Meta:
        model = models.User
        fields = ['username', 'email', 'password', 'is_superuser', 'is_staff', 'is_active', 'vote_user']

    def create(self, validated_data):
        passw = validated_data.pop('password')
        encrypt_password = make_password(passw)
        validated_data['password'] = encrypt_password
        vote_user = validated_data.pop('vote_user')
        user = models.User.objects.create(**validated_data)
        for track_data in vote_user:
            models.Profile.objects.create(uid=user, **track_data)
        return user

        # return models.User.objects.create(**validated_data)
