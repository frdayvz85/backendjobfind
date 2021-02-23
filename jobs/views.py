from django.db.models import Q
from django.shortcuts import render, redirect,get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from .forms import CommentForm, SignUpForm, ContactFormu, PostForm,JobForm,EmployerForm, AuthorForm,SignUpFormEmployer
from django.contrib.auth.models import Group
from .models import *
from django.views.generic import CreateView
# from user.forms import UserProfileForm


# Create your views here.
def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def get_employer(user):
    qs = Employer.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()

    context = {
        'queryset': queryset
    }
    return render(request, 'search_results.html', context)

def home(request):
    last_three = Testimonial.objects.all().order_by('-id')[:3]
    featured = Post.objects.filter(featured=True).order_by('-created_date')[0:3]
    comments = Comment.objects.all()
    comment_count = comments.count()
    popular_jobs = Job.objects.all().order_by('-id')[:5]
    last_three_job = Job.objects.all().order_by('-id')[:3]
    context = {
        'last_three':last_three, 'featured':featured,
        'comment_count':comment_count,
        'last_three_job':last_three_job,
        'popular_jobs':popular_jobs
        }
    return render(request, 'index.html', context)

def aboutUs(request):
    abouts = About.objects.get(pk=1)
    context = {'abouts':abouts}
    return render(request, 'about.html', context)

def foot(request):
    footers = Footer.objects.get(pk=1)
    context = {'footers':footers}
    return render(request, 'footer.html', context)    

def testimonial(request):
    testimonials = Testimonial.objects.all()
    context = {'testimonials':testimonials}
    return render(request, 'testimonials.html', context)

def team(request):
    teams = Team.objects.all()
    context = {'teams':teams}
    return render(request, 'team.html',context)

def author(request):
    authors = Author.objects.all()
    context = {'authors':authors}
    return render(request, 'author.html',context)

def term(request):
    terms = Term.objects.all()
    context = {'terms':terms}
    return render(request, 'terms.html', context)

def blog(request):
    posts = Post.objects.all()
    recent_posts = Post.objects.all().order_by('-created_date')[:3]
    tags = Tag.objects.all()
    tag_count = tags.count()
    categories = Category.objects.all()
    category_count = categories.count()
    comments = Comment.objects.all()
    comment_count = comments.count()

    paginator = Paginator(posts, 2)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1) 
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)  

    context = {
        'tags':tags,
        'categories':categories,
        'recent_posts':recent_posts,
        'comment_count':comment_count,
        'category_count':category_count,
        'tag_count':tag_count,
        'queryset': paginated_queryset,
        'page_request_var': page_request_var,
        }
    return render(request, 'blog.html', context)

def blogDetail(request, id):
    post = get_object_or_404(Post, id=id)
    recent_posts = Post.objects.all().order_by('-created_date')[:3]
    comments = Comment.objects.all()
    comment_count = comments.count()

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user =request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("blogDetail", kwargs={
                'id':post.id
            }))
    context = {
        'post':post,
        'recent_posts':recent_posts,
        'comments':comments,
        'comment_count':comment_count,
        'form':form
        }
    return render(request, 'blog-details.html', context)

@login_required(login_url='login')
def blogCreate(request):
    title='Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            messages.success(request, "Your Blog has been created succesfully. Thank you")
            return redirect(reverse("blogDetail", kwargs={
                'id':form.instance.id
            }))
    context = {
        'title':title,
        'form':form,
    }
    return render(request, 'blog-create.html', context)

@login_required(login_url='login')
def blog_update(request, id):
    title='Update'
    post = get_object_or_404(Post, id=id)
    form = PostForm(
        request.POST or None, 
        request.FILES or None, 
        instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("blogDetail", kwargs={
                'id':form.instance.id
            }))
    context = {
        'title': title,
        'form':form,
        'post':post,
    }

    return render(request, 'blog-create.html', context)

@login_required(login_url='login')
def blog_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse("blog"))



@login_required(login_url='login')
def userProfile(request):
    user = request.user
    form = AuthorForm(instance=user)
    context = {
        'form':form,
    }
    return render(request, 'user-profile.html', context)

@login_required(login_url='login')
def userProfileEdit(request):
    author = request.user.author
    form = AuthorForm(instance=author)
    if request.method == 'POST':             #form post edildiyse
        form = AuthorForm(request.POST, request.FILES, instance=author)
        if form.is_valid():
            form.save()   #veritabanina kaydet
            messages.success(request, "Your Profile has been updated succesfully.")
            return HttpResponseRedirect('userProfile')
    context = {
        'form':form,
    }
    return render(request, 'user-profile-edit.html', context)

def contact(request):
    if request.method == 'POST':             #form post edildiyse
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()            # model ile baglanti kur
            data.name = form.cleaned_data['name']  #formdan bilgiyi al
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR') #client computer ip address
            data.save()   #veritabanina kaydet
            messages.success(request, "Your Message has been sent succesfully. Thank you")
            return HttpResponseRedirect('contact')


    form = ContactFormu()

    contactInfo = ContactInfo.objects.get(pk=1)
    context = {'form':form, 'contactInfo':contactInfo}
    return render(request, 'contact.html', context)

def registerUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = SignUpForm()
        if request.method =='POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.is_user=True 
                form.save()

                Author.objects.create(
				        user=user,
				        name=user.username,
				)

                user = form.cleaned_data.get('username')
                messages.success(request, 'Profile was created succesfully for ' + user )
                return redirect('login')
                
    context = {'form':form}
    return render(request, 'register.html', context)

def registerType(request):
    return render(request, 'registertype.html')

def registerEmployer(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = SignUpForm()
        profile_form = SignUpFormEmployer(request.POST)
        if request.method =='POST':
            form = SignUpForm(request.POST)
            profile_form = SignUpFormEmployer(request.POST or None)
            if form.is_valid() and profile_form.is_valid():
                user = form.save()
                user.is_employer=True
                user.save()
                profile = profile_form.save(commit=False)
                profile.user=user
                profile.save()
                
                user = form.cleaned_data.get('username')
                messages.success(request, 'Profile was created succesfully for ' + user )
                return redirect('login')
                
    context = {
        'form':form,
        'profile_form':profile_form
        }
    return render(request, 'ceoregister.html',context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')  #also can be redirect
        else:
            messages.info(request, 'Username or Password is incorrect,Please check again')

    context = {}
    return render(request, 'login.html', context)



def logoutUser(request):
    logout(request)
    return redirect('login')








def jobs(request):
    alljob = Job.objects.all()
    type_count = alljob.count()
    context = {
        'alljob':alljob,
        'type_count':type_count
    }
    return render(request, 'jobs.html', context)

def jobDetail(request, slug):
    jobs = get_object_or_404(Job, slug=slug)
    # recent_jobs = Job.objects.all().order_by('-create_at')[:3]
    user = request.user
    form = EmployerForm(instance=user)
    # employer = get_object_or_404(Employer)
    # employer = Employer.objects.filter(name = request.user.first_name +" "+ request.user.last_name)

    context = {
        'jobs':jobs,
        # 'employer':employer,
        'form':form

        # 'recent_posts':recent_posts,
        }

    return render(request, 'job-details.html', context)


@login_required(login_url='login')
def jobCreate(request):
    title='Create'
    form = JobForm(request.POST or None, request.FILES or None)
    employer = get_employer(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.employer = employer
            form.save()
            messages.success(request, "Your Job has been created succesfully. Thank you")
            return redirect(reverse("jobDetail", kwargs={
                'slug':form.instance.slug
            }))
    context = {
        'title':title,
        'form':form,
    }
    return render(request, 'add-job.html', context)

@login_required(login_url='login')
def job_update(request, slug):
    title='Update'
    post = get_object_or_404(Job, slug=slug)
    form = JobForm(
        request.POST or None, 
        request.FILES or None, 
        instance=post)
    employer = get_employer(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.employer = employer
            form.save()
            return redirect(reverse("jobDetail", kwargs={
                'slug':form.instance.slug
            }))
    context = {
        'title': title,
        'form':form,
        'post':post,
    }

    return render(request, 'add-job.html', context)

@login_required(login_url='login')
def job_delete(request, slug):
    job = get_object_or_404(Job, slug=slug)
    job.delete()
    return redirect(reverse("jobs"))

login_required(login_url='login')
def employerProfile(request):
    user = request.user
    form = EmployerForm(instance=user)
    context = {
        'form':form,
    }
    return render(request, 'employer-profile.html', context)

@login_required(login_url='login')
def employerProfileEdit(request):
    employer = request.user.employer
    form = EmployerForm(instance=employer)
    if request.method == 'POST':             #form post edildiyse
        form = EmployerForm(request.POST, request.FILES, instance=employer)
        if form.is_valid():
            form.save()   #veritabanina kaydet
            messages.success(request, "Your Profile has been updated succesfully.")
            return HttpResponseRedirect('employerProfile')
    context = {
        'form':form,
    }
    return render(request, 'employer-profile-edit.html', context)