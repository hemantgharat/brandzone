from django.contrib import admin
from .models import Profile, Address

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    search_fields = ('user__username', 'phone')

class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'street', 'city', 'state', 'zipcode')
    search_fields = ('user__username', 'street', 'city', 'state', 'zipcode')
    list_filter = ('city', 'state')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Address, AddressAdmin)
