from django.contrib import admin
from .models import *
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.

class CustomUserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'fields': ('email', 'username','first_name','last_name', 'is_user', 'is_employer', 'password1', 'password2')
        }),
        ('Permissions', {
            'fields': ('is_superuser', 'is_staff')
        })
    )
    fieldsets = (
        (None, {
            'fields': ('email', 'username','first_name','last_name', 'is_user', 'is_employer', 'password')
        }),
        ('Permissions', {
            'fields': ('is_superuser', 'is_staff')
        })
    )
    list_display = ['email', 'username','first_name','last_name', 'is_user', 'is_employer','is_superuser']
    search_fields = ('email', 'username')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)

class AboutAdmin(admin.ModelAdmin):
    list_display = ['status','updated_date', 'created_date']
    list_filter = ['status']

    # def has_add_permission(self, request):
    #     return False
    # def has_delete_permission(self, request, obj=None):
    #     return False

admin.site.register(About, AboutAdmin)

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['fullname','updated_date', 'created_date']
    list_filter = ['fullname']

admin.site.register(Testimonial, TestimonialAdmin)

class TeamAdmin(admin.ModelAdmin):
    list_display = ['fullname','updated_date', 'created_date']
    list_filter = ['fullname']

admin.site.register(Team, TeamAdmin)

class TermAdmin(admin.ModelAdmin):
    list_display = ['title','updated_date', 'created_date']
    list_filter = ['title']

admin.site.register(Term, TermAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_filter = ['title']

admin.site.register(Tag, TagAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','featured','updated_date', 'created_date']
    list_filter = ['title']
    prepopulated_fields = {'slug':('title',)} 

admin.site.register(Post, PostAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_filter = ['title']

admin.site.register(Category, CategoryAdmin)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['user']
    list_filter = ['user']

admin.site.register(Author, AuthorAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['user']
    list_filter = ['user']

admin.site.register(Comment, CommentAdmin)

class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    list_filter = ['name']

admin.site.register(ContactFormMessage, ContactFormMessageAdmin)

class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['status', 'email']
    list_filter = ['status']

admin.site.register(ContactInfo, ContactInfoAdmin)

class FooterAdmin(admin.ModelAdmin):
    list_display = ['updated_date', 'created_date']
    list_filter = ['created_date']

    # def has_add_permission(self, request):
    #     return False
    # def has_delete_permission(self, request, obj=None):
    #     return False

admin.site.register(Footer, FooterAdmin)



class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_filter = ['title']

admin.site.register(JobCategory, JobCategoryAdmin)

class CityAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_filter = ['title']

admin.site.register(City, CityAdmin)

class JobAdmin(admin.ModelAdmin):
    list_display = ['jobtitle']
    list_filter = ['jobtitle']
    prepopulated_fields = {'slug':('jobtitle',)} 

admin.site.register(Job, JobAdmin)


class EmployerAdmin(admin.ModelAdmin):
    list_display = ['user','companyname']
    list_filter = ['name']

admin.site.register(Employer, EmployerAdmin)

