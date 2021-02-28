from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.text import slugify


# User=get_user_model()
# Create your models here.



class CustomUser(AbstractUser):
    is_user = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)


class About(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False','Hayır'),
    )
    image = models.ImageField(blank=True, upload_to='images/')
    description = RichTextUploadingField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='False')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.status

class Testimonial(models.Model):
    fullname = models.CharField(blank=True, max_length=200)
    image = models.ImageField(blank=True, upload_to='images/')
    description = RichTextUploadingField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.fullname

class Team(models.Model):
    fullname = models.CharField(blank=True, max_length=200)
    image = models.ImageField(blank=True, upload_to='images/')
    specialty = models.CharField(blank=True, max_length=200)
    facebook = models.CharField(blank=True, max_length=200)
    twitter = models.CharField(blank=True, max_length=200)
    linkedin = models.CharField(blank=True, max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.fullname

class Term(models.Model):
    title = models.CharField(max_length=3000)
    description = RichTextUploadingField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


class Footer(models.Model):
    facebook = models.CharField(blank=True, max_length=200)
    twitter = models.CharField(blank=True, max_length=200)
    behance = models.CharField(blank=True, max_length=200)
    linkedin = models.CharField(blank=True, max_length=200)
    url = models.URLField(blank=True, max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.facebook

class Employer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(upload_to='images/', default='images/default.png')
    phonenumber = models.CharField(blank=True, max_length=200)
    mobilenumber = models.CharField(blank=True, max_length=200)
    companyname = models.CharField(max_length=200)
    companyinfo = RichTextUploadingField(blank=True) 
    city = models.CharField(blank=True, max_length=200)
    website = models.CharField(blank=True, max_length=200)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username

class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(upload_to='images/', default='images/default.png')
    phonenumber = models.CharField(blank=True, max_length=200)
    profession = models.CharField(blank=True, max_length=200)


    def __str__(self):
        return self.name

class Category(models.Model):
    title=models.CharField(max_length=20)

    def __str__(self):
        return self.title

class Tag(models.Model):
    title=models.CharField(max_length=20)

    def __str__(self):
        return self.title

class Post(models.Model):
    title=models.CharField(max_length=100)
    overview=models.TextField()
    content = RichTextUploadingField()
    # comment_count=models.IntegerField(default=0)
    #view_count=models.IntegerField(default=0)
    author=models.ForeignKey(Author, on_delete=models.CASCADE)
    image = models.ImageField()
    slug = models.SlugField( null=False, unique=True)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
    featured = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blogDetail', kwargs ={
            'id':self.id
        })



    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')
    
    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class ContactFormMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
    )
    name = models.CharField(blank=True, max_length=20)
    email = models.CharField(blank=True, max_length=50)
    subject = models.CharField(blank=True, max_length=50)
    message = models.CharField(blank=True, max_length=255)
    status = models.CharField(max_length=20, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=200)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ContactInfo(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False','Hayır'),
    )
    phonenumber = models.PositiveIntegerField(blank=True)
    email = models.EmailField(max_length=50, blank=True)
    address = models.CharField(max_length=350)
    status = models.CharField(max_length=10, choices=STATUS)
    addressUrl = models.URLField(max_length=1200, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.email 


class JobCategory(models.Model):
    title=models.CharField(max_length=150)

    def __str__(self):
        return self.title
class City(models.Model):
    title=models.CharField(max_length=150)

    def __str__(self):
        return self.title
class Job(models.Model):
    TYPE = (
        ('Contract', 'Contract'),
        ('Full time', 'Full time'),
        ('Part time', 'Part time'),
    )
    ELEVEL = (
        ('Not requested', 'Not requested'),
        ('Bachelor degre', 'Bachelor degre'),
        ('Master degree', 'Master degree'),
        ('PHD degree', 'PHD degree'),
    )
    EXXPERİENCE = (
        ('Not requested', 'Not requested'),
        ('Experience > 1', 'Experience > 1'),
        ('Experience > 3', 'Experience > 3'),
        ('Experience > 5', 'Experience > 5'),
    )
    jobtitle = models.CharField(max_length=500)
    salary = models.PositiveIntegerField()
    image = models.ImageField(upload_to='images/', default='images/work2.jpg')
    overview = models.CharField(max_length=2000)
    description = RichTextUploadingField(blank=True) 
    employer=models.ForeignKey(Employer, on_delete=models.CASCADE)
    type = models.CharField(max_length=200, choices=TYPE)
    level = models.CharField(max_length=200, choices=ELEVEL)
    experience = models.CharField(max_length=200, choices=EXXPERİENCE)
    jobcategory = models.ForeignKey(JobCategory,on_delete=models.CASCADE)
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    slug = models.SlugField(null=False, unique=True, max_length=550)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.jobtitle

    def get_absolute_url(self):
        return reverse('jobDetail', kwargs ={
            'slug':self.slug
        })

    # def get_unique_slug(self):
    #     slug = slugify(self.jobtitle)
    #     unique_slug = slug
    #     counter = 1
    #     while Job.objects.filter(slug=unique_slug).exists():
    #         unique_slug = '{}-{}'.format(slug, counter)
    #         counter += 1
    #         return unique_slug

    # def save(self, *args, **kwargs):
    #     self.slug = self.get_unique_slug()
    #     return super(Job, self).save(*args, **kwargs)


class Setting(models.Model):
    websitename=models.CharField(max_length=50, null=False, blank=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.websitename
