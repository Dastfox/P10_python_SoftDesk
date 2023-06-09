from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Contributor, Project, Issue, Comment, User
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
from .permissions import IsProjectContributor, IsAuthor

####################
# ViewSets         #
####################

"""AUTHENTICATION"""


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


"""PROJECTS"""


class ProjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectContributor]
    lookup_url_kwarg = "project_id"

    def get_queryset(self):
        return Project.objects.filter(id=self.kwargs[self.lookup_url_kwarg])


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Get all projects for which the user is the author
        author_projects = Project.objects.filter(author_user=user)

        # Get all projects for which the user is a contributor
        contributed_projects = Project.objects.filter(contributors=user)

        # Combine the two sets of projects and remove duplicates
        queryset = author_projects.union(contributed_projects)

        return queryset

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data.copy()
        data["author_user"] = user.id  # set author_user to ID of authenticated user

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""COLLABORATORS"""


class ContributorListCreateView(generics.ListCreateAPIView):
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectContributor]

    def get_queryset(self):
        project_id = self.kwargs["project_id"]
        project = get_object_or_404(Project, id=project_id)
        self.check_object_permissions(self.request, project)
        return Contributor.objects.filter(project_id=project_id)

    def post(self, request, project_id):
        # Check if project exists
        project = get_object_or_404(Project, id=project_id)
        self.check_object_permissions(self.request, project)

        # Create a copy of the request data
        data = request.data.copy()

        # Set project id in the request data
        data["project"] = project.id

        # Check if contributor already exists
        try:
            contributor = Contributor.objects.get(
                user_id=request.user.id, project_id=project_id
            )

            # Update the contributor's permission if it has changed
            if contributor.permission != data["permission"]:
                contributor.permission = data["permission"]
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
            serializer = self.serializer_class(data=data)

            if serializer.is_valid():
                serializer.save(project_id=project_id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContributorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectContributor]
    lookup_url_kwarg = "user_id"

    def get_object(self):
        project_id = self.kwargs["project_id"]
        user_id = self.kwargs[self.lookup_url_kwarg]
        obj = get_object_or_404(Contributor, project_id=project_id, user_id=user_id)
        self.check_object_permissions(self.request, obj)
        return obj

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


"""ISSUES"""


class IssueListCreateView(generics.ListCreateAPIView):
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectContributor]
    lookup_url_kwarg_project = "project_id"
    lookup_url_kwarg_user = "user_id"

    def get_queryset(self):
        project_id = self.kwargs[self.lookup_url_kwarg_project]
        project = get_object_or_404(Project, id=project_id)
        self.check_object_permissions(self.request, project)

        return Issue.objects.filter(project_id=project_id)

    def post(self, request, *args, **kwargs):
        project_id = self.kwargs[self.lookup_url_kwarg_project]
        project = get_object_or_404(Project, id=project_id)
        self.check_object_permissions(self.request, project)
        data = self.request.data.copy()
        print(data)
        data[
            "author_user"
        ] = request.user.id  # set author_user to ID of authenticated user
        data["project"] = project_id  # set project to ID of project

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IssueSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsProjectContributor,
    ]
    lookup_url_kwarg = "issue_id"

    def get_object(self):
        project_id = self.kwargs["project_id"]
        project = get_object_or_404(Project, id=project_id)
        self.check_object_permissions(self.request, project)
        issue_id = self.kwargs[self.lookup_url_kwarg]
        issue = get_object_or_404(Issue, project_id=project_id, id=issue_id)
        return issue

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author_user != request.user:
            return Response(
                {"error": "Only the author of the issue can edit it."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


"""COMMENTS"""


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs["project_id"]
        project = get_object_or_404(Project, id=project_id)
        self.check_object_permissions(self.request, project)
        # Check if the user is a contributor to the project
        is_contributor = Contributor.objects.filter(
            user_id=self.request.user.id, project_id=project_id
        ).exists()

        if is_contributor:
            # Filter comments based on the issue_id
            return Comment.objects.filter(project=project_id)
        else:
            # Return an empty queryset if the user is not a contributor
            return Comment.objects.none()

    def post(self, request, *args, **kwargs):
        project_id = self.kwargs["project_id"]
        project = get_object_or_404(Project, id=project_id)
        self.check_object_permissions(self.request, project)
        issue_id = self.kwargs["issue_id"]
        issue = get_object_or_404(Issue, id=issue_id)

        self.check_object_permissions(self.request, project)
        data = self.request.data.copy()
        print(data)
        data[
            "author_user"
        ] = request.user.id  # set author_user to ID of authenticated user
        data["project"] = project_id  # set project to ID of project
        data["issue"] = issue_id  # set issue to ID of issue

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectContributor]
    lookup_url_kwarg = "comment_id"

    def get_object(self):
        project_id = self.kwargs["project_id"]
        project = get_object_or_404(Project, id=project_id)
        self.check_object_permissions(self.request, project)
        issue_id = self.kwargs["issue_id"]
        comment_id = self.kwargs[self.lookup_url_kwarg]
        obj = get_object_or_404(Comment, issue_id=issue_id, id=comment_id)
        self.check_object_permissions(self.request, obj)
        return obj

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(self.request, instance)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        project_id = self.kwargs["project_id"]
        project = get_object_or_404(Project, id=project_id)
        self.check_object_permissions(self.request, project)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
