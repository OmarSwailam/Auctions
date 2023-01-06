from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),                                             
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),                                          
    path("<str:category_name>", views.category, name="category"),
    path("add/<int:listing_id>", views.add, name="add"),
    path("remove/<int:listing_id>", views.remove, name="remove"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("close_auction/<int:listing_id>", views.close_auction, name="close_auction"),
]
