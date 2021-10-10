from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
	path("categories/<str:categories>", views.categories, name="categories"),
	path("my_watchlist", views.my_watchlist, name="my_watchlist"),
	path("listing/<str:listing>", views.listing_view, name="listing_view"),
	path("bid_to_listing/<str:listing>", views.bid_to_listing, name="bid_to_listing"),
	path("add_to_watchlist/<str:listing>", views.add_to_watchlist, name="add_to_watchlist"),	
	path("delete_listing_from_watchlist/<str:listing>", views.delete_listing_from_watchlist, name="delete_listing_from_watchlist"),
	path("close_listing/<str:listing>", views.close_listing, name="close_listing"),
	path("add_comment/<str:listing>", views.add_comment, name="add_comment"),
	path("delete_comment/<str:comment>", views.delete_comment, name="delete_comment"),
	path("my_listings/<str:user>", views.my_listings, name="my_listings"),
	path("add_listing", views.add_listing, name="add_listing"),
	path("my_winnings", views.my_winnings, name="my_winnings")
]

