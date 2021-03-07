from django.urls import path

from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('about-us/', views.aboutUs, name="about-us"),
    path('testimonials/', views.testimonial, name="testimonials"),
    path('teams/', views.team, name="teams"),
    path('terms/', views.term, name="terms"),
    path('search/', views.search, name="search"),
    path('author/<str:pk_test>', views.author, name="author"),
    path('blog/', views.blog, name="blog"),
    path('blogCreate/', views.blogCreate, name="blog-create"),
    path('blogDetail/<id>/', views.blogDetail, name="blogDetail"),
    path('blog/<id>/update/', views.blog_update, name="blog-update"),
    path('blog/<id>/delete/', views.blog_delete, name="blog-delete"),
    path('userProfile', views.userProfile, name="userProfile"),
    path('userProfileEdit', views.userProfileEdit, name="userProfileEdit"),
    path('contact', views.contact, name="contact"),
    path('login', views.loginPage, name="login"),
    path('registerType', views.registerType, name="registerType"),
    path('registerEmployer', views.registerEmployer, name="registerEmployer"),
    path('registerUser', views.registerUser, name="registerUser"),
    path('logout', views.logoutUser, name="logout"),
    path('jobs/', views.jobs,name="jobs"),
    path('jobDetail/<slug:slug>/', views.jobDetail,name="jobDetail"),
    path('jobCreate/', views.jobCreate, name="job-create"),
    path('job/<slug:slug>/update/', views.job_update, name="job-update"),
    path('job/<slug:slug>/delete/', views.job_delete, name="job-delete"),
    path('footer/', views.foot,name="footer"),

    path('employerProfile', views.employerProfile, name="employerProfile"),
    path('employerProfileEdit', views.employerProfileEdit, name="employerProfileEdit"),


     #------------ Change Password ----------------------------
    path('passwordChange',views.password_change,name='password-change'),

    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
        name="password_reset_complete"),
]