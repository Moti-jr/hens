from django.shortcuts import redirect, render 
from main_app.app_forms import ProductForm
from django.contrib import messages

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
            messages.success(request, 'product saved successfully')
            return redirect('home')  # Redirect to a view displaying the product list
    else:
        form = ProductForm()
    return render(request, 'upload_product.html', {'form': form})
