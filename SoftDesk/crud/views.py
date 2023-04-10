from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Contributor, Project, Issiue, Comment
from .serializers import (
    ContributorSerializer,
    ProjectSerializer,
    IssueSerializer,
    CommentSerializer,
    UserCreateSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from uuid import uuid4


####################
# Permissions      #
####################


class IsContributor(permissions.BasePermission):
    """
    Custom permission to only allow contributors of a project to modify it.
    """

    def has_object_permission(self, request, view, obj):
        if obj.author_user_id.id == request.user.id:
            return True

        if request.method in permissions.SAFE_METHODS:
            try:
                contributor = Contributor.objects.get(
                    user_id=request.user.id, project_id=obj.id
                )
                return (
                    contributor.permission == "user"
                    or contributor.permission == "admin"
                )
            except Contributor.DoesNotExist:
                return False

        # Write permissions are only allowed to the admin contributor of the project.
        try:
            contributor = Contributor.objects.get(
                user_id=request.user.id, project_id=obj.id
            )
            return contributor.permission == "admin"
        except Contributor.DoesNotExist:
            return False

    def has_permission(self, request, view):
        if view.action == "list":
            project_id = view.kwargs.get("project_id")
            try:
                project = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                return False
            return self.has_object_permission(request, view, project)
        elif view.action == "destroy":
            contributor_id = view.kwargs.get("pk")
            try:
                contributor = Contributor.objects.get(id=contributor_id)
            except Contributor.DoesNotExist:
                return False
            return self.has_object_permission(request, view, contributor.project)
        else:
            return True


class IsAuthor(permissions.BasePermission):
    """
    Custom permission to only allow author and admin contributors of a project to modify it.
    """

    def has_object_permission(self, request, view, obj):
        if obj.author_user_id.id == request.user.id:
            return True

        # Write permissions are only allowed to the author and admin contributors of the project.
        try:
            contributor = Contributor.objects.get(
                user_id=request.user.id, project_id=obj.id
            )
            return contributor.permission == "admin"
        except Contributor.DoesNotExist:
            return False


####################
# ViewSets         #
####################


class CustomSignupView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            )
        else:
            return Response(
                {"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class ProjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor]

    def get_queryset(self):
        return Project.objects.filter(author_user_id=self.request.user)


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(author_user_id=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author_user_id=self.request.user)


class CollaboratorListCreateView(generics.ListCreateAPIView):
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthor]

    def get_queryset(self):
        project_id = self.kwargs["project_id"]
        return Contributor.objects.filter(project_id=project_id)

    def post(self, request, project_id):
        # Check if project exists
        project = get_object_or_404(Project, id=project_id)

        # Check if contributor already exists
        try:
            contributor = Contributor.objects.get(
                user_id=request.data["user_id"], project_id=project_id
            )

            # Update the contributor's permission if it has changed
            if contributor.permission != request.data["permission"]:
                contributor.permission = request.data["permission"]
                contributor.save()

                serializer = self.serializer_class(contributor)
                return Response(serializer.data, status=status.HTTP_200_OK)

            # Return error response if contributor already exists with the same permission
            else:
                return Response(
                    {"error": "Contributor already exists with the same permission."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Create new contributor if it doesn't already exist
        except Contributor.DoesNotExist:
            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid():
                serializer.save(project_id=project_id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CollaboratorDestroyView(generics.DestroyAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor]
    lookup_url_kwarg = "pk"


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
