"""brandzone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from users.views import delete_address, login_page,register,activate_email,update_profile,view_profile,logout_user

urlpatterns = [
    path("", login_page, name="login"),
    path('register/', register, name="register"),
    path('activate/<email_token>/' , activate_email , name="activate_email"),
    path('update-profile/', update_profile, name='update-profile'),
    path("delete-address/<str:address_id>/", delete_address, name="delete-address"),
    path('profile/', view_profile, name='profile'),
    path('logout/', logout_user, name='logout'),
]
