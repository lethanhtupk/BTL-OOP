from django.urls import path, re_path
from transactions import views

urlpatterns = [
    path('wallets/',
        views.WalletList.as_view(),
        name=views.WalletList.name
    ),
    re_path('wallets/(?P<pk>[0-9]+)$',
        views.WalletDetail.as_view(),
        name=views.WalletDetail.name
    ),
    path('transactions/',
        views.TransactionList.as_view(),
        name=views.TransactionList.name
    ),
    re_path('transactions/(?P<pk>[0-9]+)$',
        views.TransactionDetail.as_view(),
        name=views.TransactionDetail.name
    ),
    path('kindoftransactions/',
        views.KindOfTransactionList.as_view(),
        name=views.KindOfTransactionList.name
    ),
    re_path('kindoftransactions/(?P<pk>[0-9]+)$',
        views.KindOfTransactionDetail.as_view(),
        name=views.KindOfTransactionDetail.name
    ),
    path('categories/',
        views.CategoryList.as_view(),
        name=views.CategoryList.name
    ),
    re_path('categories/(?P<pk>[0-9]+)$',
        views.CategoryDetail.as_view(),
        name=views.CategoryDetail.name
    ),
    path('tags/',
        views.TagList.as_view(),
        name=views.TagList.name
    ),
    re_path('tags/(?P<pk>[0-9]+)$',
        views.TagDetail.as_view(),
        name=views.TagDetail.name
    ),
    path('',
        views.ApiRoot.as_view(), 
        name=views.ApiRoot.name
    ),
    
]