from rest_framework import generics, permissions, status

from .models import Contributor, Project


class IsProjectContributor(permissions.BasePermission):
    """
    Custom permission to only allow contributors of a project to modify it.
    """

    def has_object_permission(self, request, view, obj):
        print("Checking if user is contributor")
        # Get the project_id from the obj
        if hasattr(obj, "project_id"):
            project_id = obj.project_id
        else:
            project_id = obj.id

        try:
            contributor = Contributor.objects.get(
                user_id=request.user.id, project_id=project_id
            )
            if contributor.permission == "admin" or obj.author_user == request.user:
                return True

            if contributor.permission == "user":
                return (
                    request.method in permissions.SAFE_METHODS
                    or request.method == "POST"
                )

        except Contributor.DoesNotExist:
            return obj.author_user == request.user

        return False


class IsAuthor(permissions.BasePermission):
    """
    Custom permission to only allow author and admin contributors of a project to modify it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.author_user == request.user



