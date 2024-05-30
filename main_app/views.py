from django.shortcuts import redirect, render 
from forms import ProductForm

# Create your views here.

def home(request):
    return render(request, "index.html", {})

def shop(request):
    return render(request, "shop.html", {})




def upload_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect to a view displaying the product list
    else:
        form = ProductForm()
    return render(request, 'upload_product.html', {'form': form})
