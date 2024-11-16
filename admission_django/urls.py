"""
URL configuration for admission_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from .views import register, login, logout, get_lk_content, get_all_directions, get_direction_info, add_new_direction, add_abiturient_info, add_original_diplom, get_all_abiturients, get_enrolled_abiturients

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('lk/', get_lk_content, name='lk_content'),
    path('directions/', get_all_directions, name='get_all_directions'),
    path('direction/', get_direction_info, name='get_direction_info'),
    path('directions/addNew/', add_new_direction, name='add_new_direction'),
    path('abiturients/addInfo/', add_abiturient_info, name='add_abiturient_info'),
    path('abiturients/addOriginalDiplom/', add_original_diplom, name='add_original_diplom'),
    path('abiturients/all/', get_all_abiturients, name='get_all_abiturients'),
    path('abiturients/enrolled/', get_enrolled_abiturients, name='get_enrolled_abiturients'),
]
