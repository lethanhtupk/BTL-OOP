from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import F

# Create your models here.

class Wallet(models.Model):
    name = models.CharField(max_length=255, unique=True)
    author = models.ForeignKey(
        User,
        related_name='wallets',
        on_delete=models.CASCADE,
    )
    amount = models.FloatField(validators=[MinValueValidator(0.0)])
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering = ('name',)
    
    def __str__(self): 
        return self.name

class Tag(models.Model): 
    name = models.CharField(max_length=255)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering = ('name',)

    def __str__(self):
        return self.name

class Category(models.Model): 
    name = models.CharField(max_length=255, unique=True)
    author = models.ForeignKey(
        User,
        related_name='categories',
        on_delete=models.CASCADE,
    )
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta: 
        ordering = ('name',)

    def __str__(self):
        return self.name

class KindOfTransaction(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
   

class Transaction(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='transactions',
        on_delete=models.CASCADE
    )
    wallet = models.ForeignKey(
        Wallet,
        related_name='transactions',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name='transactions', 
        on_delete=models.CASCADE,
    )
    kind = models.ForeignKey(
        KindOfTransaction, 
        related_name='transactions',
        on_delete=models.SET_NULL,
        null=True
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='transactions',
        blank=True
    )
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    amount = models.FloatField(validators=[MinValueValidator(0.0),])
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, kind=None, *args, **kwargs): 
        if kind != 'update':
            if self.kind.name == "Income":
                self.wallet.amount += self.amount
            elif self.kind.name == "Outcome":
                self.wallet.amount -= self.amount
            self.wallet.save()
            
        super(Transaction, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ('-updated_at',)

    def __str__(self):
        return self.name



