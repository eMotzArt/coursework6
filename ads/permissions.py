from rest_framework.permissions import BasePermission

class AdOwnerPermission(BasePermission):
    message = "Вы не являетесь владельцем объявления"

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        role = request.user.role

        return request.user.id == obj.author.id or role == 'admin'