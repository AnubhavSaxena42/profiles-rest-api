from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import status
from profiles_api import serializers
from rest_framework import viewsets
from profiles_api import models
from rest_framework.authentication import TokenAuthentication
from profiles_api import permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated

class HelloApiView(APIView):
    """Test Api View"""
    serializer_class = serializers.HelloSerializer

    def get(self,request,format=None):
        """Returns a list of APIView Features"""

        an_apiview = [
            'Uses HTTP methods as functions(get,post,put,patch,delete)',
            'Is similar to a traditional django view',
            'Gives you the most control over your application logic',
            'is mapped manually to urls'
        ]

        return Response({
            'message':'Hello',
            'an_apiview':an_apiview
        })

    def post(self,request):
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f"Hello, {name}"
            return Response({
                'message':message
            })
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                )

    def put(self,request,pk=None):
        """Handle updating an object"""
        return Response({
            'method:':'PUT'
        })

    def patch(self,request,pk=None):
        """Handle a partial update on an object"""
        return Response({
            'method':'PATCH'
        })

    def delete(self,request,pk=None):
        """Delete an object"""
        return Response({
            'method':'DELETE'
        })


class HelloViewSet(viewsets.ViewSet):
    """Test API View Set"""

    serializer_class = serializers.HelloSerializer

    def list(self,request):
        """Return a hello message"""

        a_viewset = [
            'Uses actions list,create,retrieve,update,partial_update',
            'Automatically maps to urls using routers',
            'Provides more functionality with less code'
        ]

        return Response({
            'message':'Hello',
            'view_set':a_viewset
        })

    def create(self,request):
        """Create a new hello message"""

        serializer=self.serializer_class(data=request.data)

        if(serializer.is_valid()):
            name=serializer.validated_data.get('name')
            message=f"Hello, {name}!"

            return Response({
                'message':message
            })

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self,request,pk=None):
        """Handle getting an object by it's ID"""

        return Response({
            'method':'GET'
        })

    def update(self,request,pk=None):
        """Handle updating an object"""

        return Response({
            'method':'PUT'
        })

    def partial_update(self,request,pk=None):
        """Handle updating a part of an object"""

        return Response({
            'method':'PATCH'
        })

    def destroy(self,request,pk=None):
        """Handle removing an object"""

        return Response({
            'method':'DELETE'
        })


class UserProfileViewset(viewsets.ModelViewSet):
    """Handle Profile CRUD"""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email',)


class UserLoginAPIView(ObtainAuthToken):
    """Handle creating user authentication tokens"""

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating reading and updating profile feed items"""
    
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (IsAuthenticated,permissions.UpdateOwnProfile)
    """permissions isAuthenticatedOrReadonly as the name suggests is used to enable other than read methods if
       a user is authenticated, furthermore we pass our custom permission which is configured to ensure that the
       authenticated user can only update their own statuses
    """
    def perform_create(self,serializer):
        """Sets the user_profile to the logged in user"""
        """Perform create is the function which we are overriding form the ModelViewSet Class
           By default it receives the data serializes and validates it, then serialize.save() function is called
           To Modify this behaviour we can use this function 
        """
        serializer.save(user_profile=self.request.user)





