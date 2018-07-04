from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Product, Review
from django.db.models import Q
from django.utils import timezone

User = settings.AUTH_USER_MODEL
# Create your views here.
def home(request):
    products=Product.objects.filter(is_public=True)
    is_upvoting=False
    return render(request, 'products/home.html',{'products':products,'is_upvoting':is_upvoting})

@login_required(login_url='login')
def create(request):
    if request.method == 'POST':
        if (request.POST.get('title') and request.POST.get('body') and request.POST.get('url') and request.FILES.get('icon') and request.FILES.get('image')):
            product = Product()
            qs = Product.objects.filter(title=request.POST['title'])
            if not qs:
                product.title = request.POST['title']
            else:
                return render(request, 'products/create.html',{'error':'Project with same name already exist'})
            product.body = request.POST['body']

            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                text = request.POST['url']
            else:
                text = 'http://' + request.POST['url']
            qs = Product.objects.filter(url__iexact=text)
            if not qs:
                product.url = text
            else:
                return render(request, 'products/create.html',{'error':'url is already added to a project'})
            if not request.POST.get('public') is None:
                product.is_public = True
            else:
                product.is_public = False
            product.icon = request.FILES['icon']
            product.image = request.FILES['image']
            product.pub_date = timezone.datetime.now()
            product.hunter = request.user
            product.save()
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 'products/create.html',{'error':'All Fields are required'})
    else:
        return render(request, 'products/create.html')

def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    is_upvoting=False
    if request.user in product.upvoters.all():
        is_upvoting=True
    return render(request, 'products/detail.html',{'product':product,'is_upvoting':is_upvoting})

@login_required(login_url='login')
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        username_to_toggle = request.POST.get("username")
        is_upvoting=False
        if request.user in product.upvoters.all():
            is_upvoting=True
        if not is_upvoting:
            product.votes_total += 1
            product.upvoters.add(request.user)
        else:
            product.votes_total -= 1
            product.upvoters.remove(request.user)
        product.save()
        return redirect('/products/' + str(product.id))

@login_required(login_url='login')
def addReview(request, product_id):
    if request.method == 'GET':
        product = get_object_or_404(Product, pk=product_id)
        review=Review()
        review.product=product
        review.author=request.user.username
        review.text = request.GET.get('q')
        review.save()
        return redirect('/products/' + str(product.id))

def search(request):
    if request.method =='GET':
        s = request.GET['q']
        s1 = request.GET['q'].capitalize()
        products=Product.objects.filter(Q(title__contains=s)|Q(title__contains=s1)|Q(hunter__username__contains=s1)|Q(hunter__username__contains=s))
        is_upvoting=False
        return render(request, 'products/home.html',{'products':products,'is_upvoting':is_upvoting})

def myproducts(request):
    products=Product.objects.filter(Q(hunter__username=request.user.username)&Q(is_public=True))
    is_upvoting=False
    return render(request, 'products/myproducts.html',{'products':products,'is_upvoting':is_upvoting})

def isPublic(request, string):
    if request.method=='POST':
        products=Product.objects.filter(Q(hunter__username=request.user.username)&Q(is_public=True))
        if string=='private':
            products=Product.objects.filter(Q(hunter__username=request.user.username)&Q(is_public=False))
        is_upvoting=False
        return render(request, 'products/myproducts.html',{'products':products,'is_upvoting':is_upvoting})

def editProduct(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method=="POST":
        if (request.POST.get('title') and request.POST.get('body') and request.POST.get('url') and request.FILES.get('icon') and request.FILES.get('image')):
            qs = Product.objects.filter(title=request.POST['title']).exclude(pk=product_id)
            if not qs:
                product.title = request.POST['title']
            else:
                return render(request, 'products/edit.html',{'error':'Project with same name already exist'})
            product.body = request.POST['body']

            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                text = request.POST['url']
            else:
                text = 'http://' + request.POST['url']
            qs = Product.objects.filter(url__iexact=text).exclude(pk=product_id)
            if not qs:
                product.url = text
            else:
                return render(request, 'products/edit.html',{'error':'url is already added to a project'})
            if not request.POST.get('public') is None:
                product.is_public = True
            else:
                product.is_public = False
            product.icon = request.FILES['icon']
            product.image = request.FILES['image']
            product.pub_date = timezone.datetime.now()
            product.hunter = request.user
            product.save()
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 'products/edit.html',{'error':'All Fields are required'})
    else:
        return render(request, 'products/edit.html',{'product':product})
