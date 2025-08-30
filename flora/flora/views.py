from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from project.models import Product,Cart,Order,Contact,Category,ProductImage
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import hashlib
from django.db.models import OuterRef, Subquery, Value, CharField, Case, When
from django.db.models.functions import Concat
from django.views.decorators.cache import cache_page
from django.utils.timezone import now
from django.contrib import messages

# myapp/views.py



def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Basic validation
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
        else:
            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()

            # Authenticate and log in the user
            user = authenticate(username=username, password=password1)
            if user is not None:
                auth_login(request, user)
                return redirect('/')

    return render(request, 'signup.html')



def user_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)  # Correct usage of the login function
            return redirect('/')
    else:
         form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('/')


def home(request):
    CLOUDINARY_BASE_URL = "https://res.cloudinary.com/dftwpyllt/"

    # Annotate with raw image path and image_url from ProductImage
    image_path_subquery = ProductImage.objects.filter(product=OuterRef('pk')).values('image')[:1]
    image_url_subquery = ProductImage.objects.filter(product=OuterRef('pk')).values('image_url')[:1]

    # Annotate first with raw image_path (can be None)
    products = Product.objects.annotate(
        image_path=Subquery(image_path_subquery, output_field=CharField()),
        image_url=Subquery(image_url_subquery, output_field=CharField())
    )

    # Annotate product_image using Case: if image_path exists, prefix with base url, else use image_url
    products = products.annotate(
        product_image=Case(
            When(image_path__isnull=False, then=Concat(Value(CLOUDINARY_BASE_URL), 'image_path')),
            default='image_url',
            output_field=CharField()
        )
    )

    # Handle search functionality
    if request.method == 'GET':
        search_query = request.GET.get('searchbox')
        if search_query:
            products = products.filter(product_name__icontains=search_query)
            print('product found actually')
            print(products)
    return render(request, 'home.html', {"product": products})


def filter_products(request,slug):


    categories = Category.objects.get(category_slug=slug)
    product = Product.objects.filter(category=categories)
    return render(request, 'home.html', {"product": product, "categories": categories})
  

def product_detail(request,slug):
    product=Product.objects.get(product_slug=slug)
    print(product)

    data={
        "product":product,
        "product_slug":slug
        
    }
    return render(request,"product_detail.html",data)



def search_suggestions(request):
    query = request.GET.get("q", "")
    print('got query')
    if query:
        products = Product.objects.filter(product_name__icontains=query)[:5]  # Use 'product_name' instead of 'name'
        suggestions = [{"name": product.product_name, "slug": product.product_slug} for product in products]
        return JsonResponse(suggestions, safe=False)
    print('searched')
    return JsonResponse([], safe=False)


@login_required
def cart(request):

    if request.user.is_authenticated:
        # Filter cart items for the authenticated user
        productitem = Cart.objects.filter(user=request.user) 
        print(productitem.all) # Fetch only user's cart items
    else:
        productitem = []  # No cart items if not authenticated
    
    return render(request, 'cart.html', {'productitem': productitem})



@login_required
def cart_add(request):
    # Support both GET and POST methods
    if request.method == 'GET':
        product_slug = request.GET.get('product_slug')

    elif request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            product_slug = data.get('product_slug')
        except (json.JSONDecodeError, AttributeError, TypeError):
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    else:
        return JsonResponse({'success': False, 'error': 'Unsupported method'}, status=405)

    if not product_slug:
        return JsonResponse({'success': False, 'error': 'Missing product_slug'}, status=400)

    product = get_object_or_404(Product, product_slug=product_slug)

    cart, created = Cart.objects.get_or_create(user=request.user, product=product)

    return JsonResponse({'success': True, 'created': created})  


def order(request, slug):
    product = get_object_or_404(Product, product_slug=slug)

    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        phoneno1 = request.POST.get('phoneno1')
        phoneno2 = request.POST.get('phoneno2')
        address = request.POST.get('address')

        if not quantity or not phoneno1 or not address:
            messages.error(request, "Please fill in all required fields.")
        else:
            try:
                total_price = int(quantity) * int(product.product_price)
                order = Order(
                    user=request.user,
                    product=product,
                    quantity=quantity,
                    phoneno1=phoneno1,
                    phoneno2=phoneno2,
                    address=address,
                    total_price=total_price
                )
                order.save()
                messages.success(request, "Your order has been placed successfully!")
            except Exception as e:
                messages.error(request, "Something went wrong while placing your order.")

        return redirect(request.path)  # reloads page to show message

    return render(request, 'order.html', {'product': product})


def contact(request):
    if request.method =='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')

        contact = Contact(
            name=name,
            email=email,
            message=message
        )
        contact.save()


    return render(request, "contact.html")
def about(request):
    return render(request,'about.html')


