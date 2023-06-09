from django.urls import path
import crud.views as views
import django.contrib.auth.views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # User registration and login
    path("auth/signup/", views.CustomSignupView.as_view(), name="signup"),
    path("auth/login/", views.CustomLoginView.as_view(), name="login"),
    # Project endpoints
    path(
        "projects/", views.ProjectListCreateView.as_view(), name="project-list-create"
    ),
    path(
        "projects/<int:project_id>/",
        views.ProjectRetrieveUpdateDestroyView.as_view(),
        name="project-detail",
    ),
    # Collaborator endpoints
    path(
        "projects/<int:project_id>/users/",
        views.ContributorListCreateView.as_view(),
        name="collaborator-list",
    ),
    path(
        "projects/<int:project_id>/users/<int:user_id>",
        views.ContributorRetrieveUpdateDestroyView.as_view(),
        name="collaborator-detail",
    ),
    # Issue endpoints
    path(
        "projects/<int:project_id>/issues/",
        views.IssueListCreateView.as_view(),
        name="issue-list-create",
    ),
    path(
        "projects/<int:project_id>/issues/<int:issue_id>/",
        views.IssueRetrieveUpdateDestroyView.as_view(),
        name="issue-detail",
    ),
    # Comment endpoints
    path(
        "projects/<int:project_id>/issues/<int:issue_id>/comments/",
        views.CommentListCreateView.as_view(),
        name="comment-list-create",
    ),
    path(
        "projects/<int:project_id>/issues/<int:issue_id>/comments/<int:comment_id>/",
        views.CommentRetrieveUpdateDestroyView.as_view(),
        name="comment-detail",
    ),
]
