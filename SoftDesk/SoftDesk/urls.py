from django.urls import path
import crud.views as views
import django.contrib.auth.views

urlpatterns = [
    # User registration and login
    path("login/",  django.contrib.auth.views.LoginView.as_view(), name="login"),
    path("signup/", django.contrib.auth.views.LoginView.as_view(), name="signup"),
    # Project endpoints
    path(
        "projects/", views.ProjectListCreateView.as_view(), name="project-list-create"
    ),
    path(
        "projects/<int:pk>/",
        views.ProjectRetrieveUpdateDestroyView.as_view(),
        name="project-detail",
    ),
    # Collaborator endpoints
    path(
        "projects/<int:project_id>/users/",
        views.CollaboratorCreateView.as_view(),
        name="collaborator-create",
    ),
    path(
        "projects/<int:project_id>/users/",
        views.CollaboratorListView.as_view(),
        name="collaborator-list",
    ),
    path(
        "projects/<int:project_id>/users/<int:user_id>",
        views.CollaboratorDestroyView.as_view(),
        name="collaborator-delete",
    ),
    # Issue endpoints
    path(
        "projects/<int:project_id>/issues/",
        views.IssueListCreateView.as_view(),
        name="issue-list-create",
    ),
    path(
        "projects/<int:project_id>/issues/<int:pk>/",
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
        "projects/<int:project_id>/issues/<int:issue_id>/comments/<int:pk>/",
        views.CommentRetrieveUpdateDestroyView.as_view(),
        name="comment-detail",
    ),
]
