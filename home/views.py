from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Product, Comment
from .forms import ProductForm, CommentForm


class Home(View):
    def get(self, request):
        products = Product.objects.all()[:3]
        return render(request, 'home/home.html', {'products':products})


class Products(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        q = request.GET.get('q')
        user = request.user
        if q:
            products = Product.objects.filter(Q(name__icontains=q) | Q(price__icontains=q))
        else:
            product = Product.objects.all()
            paginator = Paginator(product, 3)
            page_number = request.GET.get("page")
            products = paginator.get_page(page_number)
        return render(request, 'home/products.html', {'products': products, 'user': user})


class About(View):
    def get(self, request):
        return render(request, 'home/about.html')


class Contact(View):
    def get(self, request):
        return render(request, 'home/contact.html')


class ProductDetail(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        comments = Comment.objects.filter(product=product).order_by('-created_at')
        context = {'product': product, 'comments': comments}
        return render(request, 'home/product_detail.html', context)


class ProductCreate(View):
    def get(self, request):
        form = ProductForm()
        products = Product.objects.all()
        return render(request, 'home/product_create.html', {'products': products, 'form': form})
    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')
        return render(request, 'home/product_create.html', {'form': form})


class ProductUpdateView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        form = ProductForm(instance=product)
        context = {'form': form, 'product': product}
        return render(request, 'home/product_update.html', context)

    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('detail', pk=product.pk)
        return render(request, 'home/product_update.html', {'form': form, 'product': product})



class PhoneDeleteView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        context = {'product': product}
        return render(request, 'home/product_delete.html', context)

    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        product.delete()
        return redirect('products')


class CommentView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        form = CommentForm()
        context = {'form': form, 'product': product}
        return render(request, 'home/comment.html', context)

    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()
            return redirect('detail', pk=pk)
        return render(request, 'home/comment.html', {'form': form, 'product': product})

