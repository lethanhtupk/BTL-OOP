from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from .models import UserProfile
from .serializers import UserProfileSerializer
from .custompermissions import IsOwnerUserProfileOrReadOnly

# Create your views here.

class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    name = 'profile-list'
    permission_classes = (
        permissions.IsAdminUser,
    )

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)    

class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    name = 'profile-detail'
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerUserProfileOrReadOnly,
    )
