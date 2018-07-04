from django.urls import path
from . import views
urlpatterns = [
    path('create',views.create, name='create'),
    path('<int:product_id>/edit',views.editProduct, name='edit'),
    path('<int:product_id>',views.detail, name='detail'),
    path('<int:product_id>/upvote',views.upvote,name='upvote'),
    path('<int:product_id>/add_review',views.addReview,name='add_review'),
    path('results',views.search,name='search'),
    path('myproducts',views.myproducts, name='my_products'),
    path('<string>/ispublic',views.isPublic, name='isPublic')
]
