from rest_framework.permissions import BasePermission
from InstaTonneApis.endpoints.utils import check_auth_header

class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        return check_auth_header(request)
