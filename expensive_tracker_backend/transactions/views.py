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
# Create your views here.

class WalletList(generics.ListCreateAPIView):
    queryset = Wallet.objects.all() 
    serializer_class = WalletSerializer
    name = 'wallet-list'

    # def perform_create(self, serializer): 
    #     serializer.save(author=self.request.user)

class WalletDetail(generics.RetrieveUpdateDestroyAPIView): 
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    name = 'wallet-detail'

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all() 
    serializer_class = CategorySerializer
    name = 'category-list'

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    name = 'category-detail'

class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    name = 'transaction-list'

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)
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

    
class KindOfTransactionList(generics.ListCreateAPIView): 
    queryset = KindOfTransaction.objects.all()
    serializer_class = KindOfTransactionSerializer
    name = 'kindoftransaction-list'

class KindOfTransactionDetail(generics.RetrieveUpdateDestroyAPIView): 
    queryset = KindOfTransaction.objects.all()
    serializer_class = KindOfTransactionSerializer
    name = 'kindoftransaction-detail'

class TagList(generics.ListCreateAPIView):
    queryset= Tag.objects.all() 
    serializer_class = TagSerializer
    name = 'tag-list'
    # permission_classes = (
    #     permissions.IsAuthenticatedOrReadOnly,
    # )

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
    # permission_classes = (
    #     permissions.IsAuthenticatedOrReadOnly,
    #     custompermission.IsAdminOrReadOnly,
    # )


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