from django.shortcuts import *
from app.models import *
from django.contrib.auth import *
from app.models import *
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib.auth.models import *
from app.models import User, Order

def Master(request):
    return render(request, "masters.html")


def Index(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()

    categoryID = request.GET.get('category')
    subcategoryID = request.GET.get('subcategory')
    brandID = request.GET.get('brand')

    # Apply filters based on user selection
    if subcategoryID:
        product = Product.objects.filter(sub_category__id=subcategoryID)
    elif categoryID:
        product = Product.objects.filter(category__id=categoryID)
    elif brandID:
        product = Product.objects.filter(brand__id=brandID)
    else:
        product = Product.objects.all()

    context = {
        'categories': categories,
        'product': product,
        'brands': brands,
    }
    return render(request, "index.html", context)



def signup(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()  # Save the user first
            # Authenticate using correct credentials
            authenticated_user = authenticate(
                username=new_user.username,  # Use new_user.username
                password=request.POST["password1"],  # Directly access password1
            )
            if authenticated_user is not None:  # Ensure authentication works
                login(request, authenticated_user)  # Log in the user
                return redirect('/')  # Redirect to home page
    else:
        form = UserCreateForm()

    context = {'form': form}
    return render(request, 'registration/signup.html', context)


@login_required(login_url="/account/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="/account/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/account/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/account/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/account/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/account/login/")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')

def Conctact_Page(request):
    if request.method == "POST":
        contact = Contact_us(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
        )
        contact.save()
    return render(request,'contact.html')
def Checkout(request):
    if request.method == "POST":
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        pincode = request.POST.get('pincode')

        cart = request.session.get('cart', {})

        if not cart:
            return HttpResponse("Cart is empty. Please add items before checkout.")

        uid = request.session.get('_auth_user_id')
        user = User.objects.get(pk=uid)

        print(address, phone, pincode, cart, user)

        for i in cart:
            # 🔹 Ensure price and quantity are retrieved correctly
            a = float(cart[i].get('price', 0))  # ✅ Ensure it's a float
            b = int(cart[i].get('quantity', 1))  # ✅ Ensure it's an integer

            total = a * b  # ✅ Correct multiplication

            order = Order(
                user=user,
                product=cart[i]['name'],
                quantity=b,
                price=a,
                total_price=total,  # ✅ Store total price (Ensure 'total_price' exists in Order model)
                image=cart[i].get('image', ''),
                address=address,
                phone=phone,
                pincode=pincode,
            )
            order.save()
        request.session['cart'] = {}
        return redirect("index")

    return HttpResponse("This is the checkout page.")


def Your_order(request):
    uid = request.session.get('_auth_user_id')  # Get user ID from session
    user = User.objects.get(pk=uid)  # Get the user

    order = Order.objects.filter(user=user)  # Get user orders

    print(order)  # 🔹 Print in terminal to check if orders are fetched correctly

    context = {
        'order': order,
    }
    return render(request, 'order.html', context)


def Product_page(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()

    # Get filter parameters
    categoryID = request.GET.get('category')
    subcategoryID = request.GET.get('subcategory')
    brandID = request.GET.get('brand')

    try:
        categoryID = int(categoryID) if categoryID else None
        subcategoryID = int(subcategoryID) if subcategoryID else None
        brandID = int(brandID) if brandID else None
    except ValueError:
        categoryID = None
        subcategoryID = None
        brandID = None

    # Start with all products
    products = Product.objects.all()

    # Apply filters
    if categoryID:
        products = products.filter(category__id=categoryID)
    if subcategoryID:
        products = products.filter(sub_category__id=subcategoryID)
    if brandID:
        products = products.filter(brand__id=brandID)

    print(f"Filtered Products: {products}")  # Debugging output
    print(f"SQL Query: {products.query}")  # Debugging output

    context = {
        'categories': categories,
        'products': products,  # ✅ Use 'products' in the template
        'brands': brands,
        'categoryID': categoryID,  # ✅ Pass to template for active state
        'subcategoryID': subcategoryID,
        'brandID': brandID,
    }
    return render(request, 'product.html', context)


from django.shortcuts import render, get_object_or_404

def Product_detail(request, id):  # 🔹 Accept 'id' as a parameter
    product = get_object_or_404(Product, id=id)  # 🔹 Safely fetch product or return 404
    return render(request, 'product_detail.html', {'product': product})

def Search(request):
    query = request.GET['query']
    product = Product.objects.filter(name__icontains=query)
    context = {'product': product}
    return render(request,'search.html',context)
