from django.conf.urls.static import static
from django.urls import path
from clothes import settings
from .views import Home, Products, About, Contact, ProductDetail, ProductCreate, CommentView, ProductUpdateView, ProductDeleteView

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('products/', Products.as_view(), name='products'),
    path('about/', About.as_view(), name='about'),
    path('contact/', Contact.as_view(), name='contact'),
    path('product/<int:pk>', ProductDetail.as_view(), name='detail'),
    path('product/create/', ProductCreate.as_view(), name='create'),
    path('comment/<int:pk>', CommentView.as_view(), name='comment'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='update'),
    path('phone/<int:pk>/delete/', ProductDeleteView.as_view(), name='delete'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)