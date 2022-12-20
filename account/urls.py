from django.urls import path
from account.views import (UserRegistrationView,UserLoginView,UserProfileView,
    UserChangePasswordView,SendPasswordChangeEmailView,UserPasswordResetView,CreateMenuGrpView,
    UpdateMenuGrpView,UpdateMenuMasterView,CreateMenuMasterView,CreateTaskMasterView,UpdateTaskMasterView,CreateUserTaskAccessView,
    UpdateUserTaskAccessView,CreateFieldMasterView,UpdateFieldMasterView,CreateTaskFieldMasterView,UpdateTaskFieldMasterView)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('passwordchange/', UserChangePasswordView.as_view(), name='passwordchange'),
    path('resetpassmail/', SendPasswordChangeEmailView.as_view(), name='resetpassmail'),
    path('resetpassword/<uid>/<token>/', UserPasswordResetView.as_view(), name='resetpassword'),
    path('menuview/',CreateMenuGrpView.as_view(), name='menuview'),
    path('menuview/<int:pk>',UpdateMenuGrpView.as_view(), name='menuviewupdate'),
    path('menumasterview/',CreateMenuMasterView.as_view(), name='menumasterview'),
    path('menumasterview/<int:pk>',UpdateMenuMasterView.as_view(), name='menumasterviewupdate'),
    path('taskmasterview/',CreateTaskMasterView.as_view(), name='taskmasterview'),
    path('taskmasterview/<int:pk>',UpdateTaskMasterView.as_view(), name='taskmasterviewupdate'),
    path('usertaskaccessview/',CreateUserTaskAccessView.as_view(), name='usertaskaccessview'),
    path('usertaskaccessview/<int:pk>',UpdateUserTaskAccessView.as_view(), name='usertaskaccessviewupdate'),
    path('fieldmasterview/',CreateFieldMasterView.as_view(), name='fieldmasterview'),
    path('fieldmasterview/<int:pk>',UpdateFieldMasterView.as_view(), name='fieldmasterviewupdate'),
    path('taskfieldmasterview/',CreateTaskFieldMasterView.as_view(), name='taskfieldmasterview'),
    path('taskfieldmasterview/<int:pk>',UpdateTaskFieldMasterView.as_view(), name='taskfieldmasterviewupdate'),

]