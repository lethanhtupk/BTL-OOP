from django.db.models import F
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status
from transactions.models import (
    Category,
    Tag,
    Transaction,
    KindOfTransaction,
    Wallet
)
from transactions.serializers import (
    CategorySerializer,
    TagSerializer,
    TransactionSerializer,
    WalletSerializer,
    KindOfTransactionSerializer
)
from django_filters import rest_framework as filters
from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter
from rest_framework import permissions
from transactions import custompermission
from django.http import Http404

class WalletList(generics.ListCreateAPIView):
    queryset = Wallet.objects.all() 
    serializer_class = WalletSerializer
    name = 'wallet-list'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer): 
        serializer.save(author=self.request.user)

class WalletDetail(generics.RetrieveUpdateDestroyAPIView): 
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    name = 'wallet-detail'
    # only author can update wallet
    permission_classes = (
        custompermission.IsAuthorOrReadOnly,
    )

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all() 
    serializer_class = CategorySerializer
    name = 'category-list'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    name = 'category-detail'
    permission_classes = (
        custompermission.IsAuthorOrReadOnly,
    )

class TransactionFilter(filters.FilterSet):
    from_date = DateTimeFilter(
      field_name='created_at', lookup_expr='gte'
    )
    to_date = DateTimeFilter(
      field_name='created_at', lookup_expr='lte'
    )

    class Meta: 
      model = Transaction
      fields = (
            'wallet',
            'category',
            'from_date',
            'to_date',
          )

class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    name = 'transaction-list'
    filter_class = TransactionFilter
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    @staticmethod
    def check_amount(data): 
        wallet = Wallet.objects.get(name=data['wallet'])
        if wallet.amount >= data['amount']:
            return True
        return False

    def create(self, request, *args, **kwargs): 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if self.check_amount(request.data):
            self.perform_create(serializer)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            data={'amount': 'The amount of transaction cannot be greater than the amount of wallet'},
            status=status.HTTP_400_BAD_REQUEST
        )


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all() 
    serializer_class = TransactionSerializer
    name = 'transaction-detail'
    permission_classes = (
        custompermission.IsAuthorOrReadOnly,
    )

    def destroy(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        try: 
            instance = self.get_object()
            wallet_instance = instance.wallet
            if instance.KindOfTransaction.name == "Outcome":
                wallet_instance.amount = wallet_instance.amount + instance.amount
            elif instance.KindOfTransaction.name == "Income":
                wallet_instance.amount = wallet_instance.amount - instance.amount
            wallet_instance.save()
            self.perform_destroy(instance)
        except:
            return Response(data={'message': 'Cannot find transaction!'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data={'message': 'Delete success!'}, status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        try:
            instance = self.get_object()
            wallet_instance = instance.wallet
            amountBefore = instance.amount
            kindOfTransBefore = instance.kind.name
            amountAfter = request.data['amount']
            if kindOfTransBefore == "Income":
                if instance.kind.name == "Income":
                    amount_diff = amountAfter - amountBefore
                elif instance.kind.name == "Outcome":
                    amount_diff = - (amountAfter + amountBefore)
            elif kindOfTransBefore == "Outcome":
                if instance.kind.name == "Outcome":
                    amount_diff = amountBefore - amountAfter
                elif instance.kind.name == "Income":
                    amount_diff = amountBefore + amountAfter
            if instance.wallet.amount + amount_diff > 0:
                instance.wallet.amount += amount_diff
            else:
                return Response(data={'message': "The wallet amount doesn't have enough!"}, status=status.HTTP_400_BAD_REQUEST)
            instance.wallet.save()
        except Http404:
            return Response(data={'message': 'Cannot find transaction!'}, status=status.HTTP_404_NOT_FOUND)
        return super(TransactionDetail, self).update(request, *args, **kwargs)


    
class KindOfTransactionList(generics.ListCreateAPIView): 
    queryset = KindOfTransaction.objects.all()
    serializer_class = KindOfTransactionSerializer
    name = 'kindoftransaction-list'
    permission_classes = (
        permissions.IsAdminUser
    )

class KindOfTransactionDetail(generics.RetrieveUpdateDestroyAPIView): 
    queryset = KindOfTransaction.objects.all()
    serializer_class = KindOfTransactionSerializer
    name = 'kindoftransaction-detail'
    permission_classes = (
        permissions.IsAdminUser,
    )

class TagList(generics.ListCreateAPIView):
    queryset= Tag.objects.all() 
    serializer_class = TagSerializer
    name = 'tag-list'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    @staticmethod
    def check_tag(data): 
        tag = Tag.objects.all().filter(name=data['name'])
        if tag:
            return True
        return False

    def create(self, request, *args, **kwargs): 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if self.check_tag(request.data) == False:
            self.perform_create(serializer)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            data={'name': 'tag with this name already exists.'},
            status=status.HTTP_400_BAD_REQUEST
        )

class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset= Tag.objects.all() 
    serializer_class = TagSerializer
    name = 'tag-detail'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        custompermission.IsAdminOrReadOnly,
    )


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({
            'wallets': reverse(WalletList.name, request=request),
            'categories': reverse(CategoryList.name, request=request),
            'tags': reverse(TagList.name, request=request),
            'transactions': reverse(TransactionList.name, request=request),
            'kindoftransactions': reverse(KindOfTransactionList.name, request=request),
        })
