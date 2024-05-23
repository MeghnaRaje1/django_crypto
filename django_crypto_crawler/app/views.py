from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm
from .models import HistoricalData
from django.http import JsonResponse

def product_list(request):
    print("Inside product list")
    products = Product.objects.all()
    print(products)
    return render(request, 'product_list.html', {'products': products})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('product_list')



from datetime import datetime

def historical_data_view(request):
    # Query the HistoricalData model, ordering by timestamp in descending order
    historical_data = HistoricalData.objects.all().order_by('-timestamp')
   
    data = [
        {
            'product': item.product.name,
            'timestamp': item.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'open': item.open,
            'high': item.high,
            'low': item.low,
            'close': item.close
        }
        for item in historical_data
    ]


    context = {
        'historical_data': data
    }
    # Render the HTML template with the queried data
    return render(request, 'historical_data.html', context)

def historical_data_json(request):
    # Query the HistoricalData model, ordering by timestamp in descending order
    historical_data = HistoricalData.objects.all().order_by('-timestamp')
    # print(historical_data)

    # Prepare the data in a JSON-serializable format with formatted timestamps
    data = [
        {
            'product': item.product.name,
            'timestamp': item.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'open': item.open,
            'high': item.high,
            'low': item.low,
            'close': item.close
        }
        for item in historical_data
    ]
    # Return the data as a JSON response
    return JsonResponse({'data': data})
