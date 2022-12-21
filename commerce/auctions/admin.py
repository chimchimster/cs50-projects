from django.contrib import admin
from .models import User, Listings, WatchList, Bids

# Register your models here.
admin.site.register(User)
admin.site.register(Listings)
admin.site.register(WatchList)
admin.site.register(Bids)
