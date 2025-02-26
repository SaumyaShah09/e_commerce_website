from django.shortcuts import *
from app.models import *
from django.contrib.auth import *
from app.models import *
def Master(request):
    return render(request, "masters.html")


def Index(request):
    categories = Category.objects.all()
    categoryID = request.GET.get('category')
    if categoryID:
        product = Product.objects.filter(sub_category=categoryID)
    else:
        product = Product.objects.all()

    context = {
        'categories': categories,
        'product': product,
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