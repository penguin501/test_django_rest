# coding: utf-8

from rest_framework import serializers

from .models import User, Entry


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'mail',)
        extra_kwargs = {
            'name': {'read_only': False},
            'mail': {'read_only': False},
        }


class EntrySerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Entry
        fields = ('title', 'body', 'created_at', 'status', 'author',)
        read_only_fields = ('created_at',)

    def create(self, validated_data):
        user_data = validated_data.pop('author')
        user = User.objects.get(name=user_data['name'])
        post = Entry.objects.create(author=user, **validated_data)
        return post
