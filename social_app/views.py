from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from social_app.forms import RegistrationForm, EditUserProfileForm
from social_app.models import CustomUser, Follow, Post, UserProfile
from django.contrib import messages


# Create your views here.




class RegisterView(View):
    def get(self,request):
        form = RegistrationForm()
        return render(request, 'register.html', {"form": form})

    def post(self,request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            if CustomUser.objects.filter(username=username).exists():
                return render(request, 'registration.html', {'form': form, 'error': 'Username already exists.'})


            user = CustomUser.objects.create_user(username=username, password=password)

            return redirect('login')
        else:
            return render(request, 'registration.html', {'form': form})



class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            print('valid here')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            return render(request, 'login.html', {'form': form, 'error': 'Invalid credentials'})




class HomeView(View):
    def get(self, request):

        current_user = request.user

        followed_users = Follow.objects.filter(follower=current_user).values_list('followed', flat=True)
        print(followed_users,'......followed user')
        posts = Post.objects.filter(user__in=followed_users).order_by('-created_at')

        return render(request, 'home.html', {'posts': posts})


class UserProfileView(View):
    def get(self, request, username):
        profile_user = get_object_or_404(CustomUser, username=username)
        profile, created = UserProfile.objects.get_or_create(user=profile_user,
                                                             defaults={'bio': '', 'profile_picture': None})
        user_posts = Post.objects.filter(user=profile_user).order_by('-created_at')
        followers_count = profile_user.followers.count()
        followed_users_count = profile_user.followed_users.count()

        edit_profile_form = EditUserProfileForm(instance=profile)

        return render(request, 'profile.html', {'profile': profile, 'user_posts': user_posts,
                                                'followers_count': followers_count,
                                                'followed_users_count': followed_users_count,
                                                'edit_profile_form': edit_profile_form})

    def post(self, request, username):
        profile_user = get_object_or_404(CustomUser, username=username)
        profile, created = UserProfile.objects.get_or_create(user=profile_user,
                                                             defaults={'bio': '', 'profile_picture': None})
        user_posts = Post.objects.filter(user=profile_user).order_by('-created_at')
        followers_count = profile_user.followers.count()
        followed_users_count = profile_user.followed_users.count()

        edit_profile_form = EditUserProfileForm(request.POST, request.FILES, instance=profile)
        if edit_profile_form.is_valid():
            edit_profile_form.save()
            return redirect('user_profile', username=username)

        return render(request, 'profile.html', {'profile': profile, 'user_posts': user_posts,
                                                'followers_count': followers_count,
                                                'followed_users_count': followed_users_count,
                                                'edit_profile_form': edit_profile_form})



class FollowView(View):
    def get(self, request, username):
        user_to_follow = get_object_or_404(CustomUser, username=username)
        Follow.objects.create(follower=request.user, followed=user_to_follow)
        messages.success(request, f"You are now following {user_to_follow.username}")
        return redirect('user_profile', username=username)

class UnfollowView(View):
    def get(self, request, username):
        user_to_unfollow = get_object_or_404(CustomUser, username=username)
        Follow.objects.filter(follower=request.user, followed=user_to_unfollow).delete()
        messages.warning(request, f"You have unfollowed {user_to_unfollow.username}")
        return redirect('user_profile', username=username)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')