from django.urls import path

from social_app.views import RegisterView, LoginView, HomeView, UserProfileView, LogoutView, FollowView, UnfollowView

urlpatterns = [
    path('', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='user_profile'),
    path('follow/<str:username>/', FollowView.as_view(), name='follow'),
    path('unfollow/<str:username>/', UnfollowView.as_view(), name='unfollow'),
    path('logout/', LogoutView.as_view(), name='logout')

]