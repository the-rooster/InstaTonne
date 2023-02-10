"""InstaTonne URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework.schemas import get_schema_view

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('openapi', get_schema_view(
        title="InstaTonne API",
        description="This will show schema info for everything in urlpatterns (in urls.py)",
        version="1.0.0" # We will probably not update this unless we make API changes later
        # url='https://www.example.org/api/' <- if we want a custom url for a schema, add it here
        # urlconf=ROOT_URLCONF <- ROOT_URLCONF is default, so we probably won't need to add this
    ), name='openapi-schema'), 
]

# schema_generator.get_schema() can be used to get a JSON object containing the same data, in case we need to export it:
# (This JSON is identical to the one generated above with get_schema_view)
# Note: this grabs data from urlpatterns using Django magic, so needs to be after it in this file

# from rest_framework.schemas.openapi import SchemaGenerator
# schema_generator = SchemaGenerator(title='InstaTonne API',
#         description="This will print schema info for everything in urlpatterns (in urls.py)",
#         version="1.0.0" # We will probably not update this unless we make API changes later
#         # url='https://www.example.org/api/' <- if we want a custom url for a schema, add it here
#         # urlconf=ROOT_URLCONF <- ROOT_URLCONF is default, so we probably won't need to add this
#     )
# print(schema_generator.get_schema())