from django.urls import path, re_path

from .views import UserProfileList, UserProfileDetail

urlpatterns = [
    #gets all user profiles and create a new profile
    path("profiles/", UserProfileList.as_view(), name=UserProfileList.name),
    # retrieves profile details of the currently logged in user
    path("profiles/<int:pk>", UserProfileDetail.as_view(), name=UserProfileDetail.name),
]