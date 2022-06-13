"""
Views for the user API.
"""
from rest_framework import generics

from user.serializers import UserSerializer


# CreateAPIView handles http post request for creating objects
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    # a lot of logic for creating object in db is handled, and only need
    # to define a serializer, and set the serializer class on this view
    serializer_class = UserSerializer
