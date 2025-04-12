#__________________________________________________________________#
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from .search import result
from django.contrib import messages
from .models import Search,user,Ads,Ads_3rd_Party,UserActivity,gen_notification,per_notification,contact_us
from .forms import loginform,Payment_details
from django.contrib.auth import authenticate,login
#__________________________________________________________________#
def index(request):
    return render(request, 'index.html')
#__________________________________________________________________#
def search(request):
    if request.method == 'POST':
        query = request.POST.get('search', '').strip()
        if not query:
            messages.error(request, 'Please enter a search query.')
            return redirect('index')
        try:
            result_link, result_text, result_para = result(query)
            result_data = zip(result_link, result_text, result_para)
            
            # Save search only for authenticated users
            if request.user.is_authenticated:
                res = Search(query=query, result_link=result_link, user=request.user)
                res.save()
            
            # Fetch ad safely
            random_ad = Ads_3rd_Party.objects.first()
            
            if not result_link:  # Check if results are empty
                messages.warning(request, 'No results found.')
                return render(request, 'search.html', {'results': [], 'random_ad': random_ad})
            return render(request, 'search.html', {'results': result_data, 'random_ad': random_ad})
        except Exception as e:
            messages.error(request, f'Error processing search: {str(e)}')
            return render(request, 'search.html', {'results': [], 'random_ad': None})
    return redirect('index')
        
#__________________________________________________________________#
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')  
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')   
        password = request.POST.get('password')
        if user.objects.filter(username=username).exists() or user.objects.filter(email=email):
            messages.error(request,'Username/Email Already Exists')
            return redirect('register')
        user_ = user.objects.create_user(username=username,email=email,first_name=first_name,last_name=last_name,password=password,)
        user_.save()
        messages.success(request,'User Created Sucessfully')
        return redirect('login')
    return render(request, 'Users/register.html')
#__________________________________________________________________#
def Login(request):
    form = loginform(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username= form.cleaned_data.get('username')
            password= form.cleaned_data.get('password')
            User = authenticate(request,username=username,password=password)
            if User is not None:
                login(request,User)
                return redirect('index')
            else:
                messages.error(request,'invalid credentials')
        else:
            messages.error(request,'error validating form')
    return render(request, 'Users/login.html',{'form':form})
#__________________________________________________________________#
def history(request):
    past = Search.objects.filter(user=request.user).order_by('-date')
    context = {
        'past':past
    }
    return render(request,'history.html',context)
#__________________________________________________________________#
def profile(request):
    guy = request.user
    user_ = user.objects.filter(username=guy).first()
    user_time = UserActivity.objects.filter(user=request.user)
    context = {
        'user':user_,
        'user_time':user_time
    }
    return render(request, 'Users/profile.html',context)
#__________________________________________________________________#
def edit_profile(request, user_id):
    User_ = get_object_or_404(user, pk=user_id)
    if request.method == 'POST':
        User_.email = request.POST['email']
        User_.description = request.POST['description']
        User_.image = request.POST['image']
        User_.save()        
        return redirect('profile') 
    context = {
    'User': User_,
    }
    return render(request, 'Users/edit_profile.html',context) 
#__________________________________________________________________#
def edit_payment_info(request, user_id):
    User_ = get_object_or_404(user, pk=user_id)
    if request.method == 'POST':
        User_.payment_method = request.POST['payment_method']
        User_.payment_info = request.POST['payment_info']
        User_.save()        
        return redirect('profile') 
    context = {
    'User': User_,
    }
    return render(request, 'Users/edit_payments.html',context) 
#__________________________________________________________________#

def notifications_view(request):
    # Fetching notifications from the database
    general_notifications = gen_notification.objects.all()
    personal_notifications = per_notification.objects.all()
    context = {
        'general': general_notifications,
        'personal': personal_notifications,
    }
    return render(request, 'base.html', context)

def about_us(request):
    return render(request,'Pages/about_us.html')

def contact(request):
    if request.method== 'POST':
        desc = request.POST['description']
        a_user = request.user
        contact_ = contact_us(user=a_user,message=desc)
        contact_.save()
    return render(request,'Pages/contact_us.html')