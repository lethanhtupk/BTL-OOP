from django.contrib import admin
from .models import Wallet
from .models import Tag
from .models import Category
from .models import KindOfTransaction
from .models import Transaction

# Register your models here.
admin.site.register(Wallet)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(KindOfTransaction)
admin.site.register(Transaction)
