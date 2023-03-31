from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Contributor, Project, Issiue, Comment
from .serializers import (
    ContributorSerializer,
    ProjectSerializer,
    IssueSerializer,
    CommentSerializer,
)


# Add your views here (examples provided for a few views)
class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]


# Repeat this process for each of your views, updating the queryset, serializer_class, and permissions as needed.
# Replace the existing ProjectListCreateView with this one
class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(author_user_id=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author_user_id=self.request.user)


# Add the remaining views
# Collaborator views
class CollaboratorCreateView(generics.CreateAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]


class CollaboratorListView(generics.ListAPIView):
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs["project_id"]
        return Contributor.objects.filter(project_id=project_id)


class CollaboratorDestroyView(generics.DestroyAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "user_id"


# Issue views
class IssueListCreateView(generics.ListCreateAPIView):
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs["project_id"]
        return Issiue.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        serializer.save(
            project_id=self.kwargs["project_id"], author_user_id=self.request.user
        )


class IssueRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs["project_id"]



class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        issue_id = self.kwargs["issue_id"]
        return Comment.objects.filter(issue_id=issue_id)

    def perform_create(self, serializer):
        issue = get_object_or_404(Issiue, id=self.kwargs["issue_id"])
        serializer.save(author_user_id=self.request.user, issue_id=issue)


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        issue_id = self.kwargs["issue_id"]
        return Comment.objects.filter(issue_id=issue_id)
