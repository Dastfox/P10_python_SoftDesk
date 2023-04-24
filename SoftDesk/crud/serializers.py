from rest_framework import serializers
from .models import Contributor, Project, Issue, Comment, User
from django.contrib.auth.forms import UserCreationForm


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = "__all__"
        extra_kwargs = {
            "project": {"write_only": True},
        }


class ProjectSerializer(serializers.ModelSerializer):
    author_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, required=False
    )

    id = serializers.IntegerField(required=False)

    class Meta:
        model = Project
        fields = "__all__"
        extra_kwargs = {
            "author_user": {"write_only": True},
        }


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class UserCreateSerializer(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
