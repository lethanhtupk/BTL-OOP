from rest_framework import serializers
from transactions.models import (
    Wallet,
    Category, 
    Tag, 
    Transaction, 
    KindOfTransaction,
)

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    transactions = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='transaction-detail'
    )
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Category
        fields = (
            'url',
            'pk',
            'name',
            'author',
            'transactions',
            'created_at',
            'updated_at',
        )

class WalletSerializer(serializers.HyperlinkedModelSerializer):
    transactions = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='transaction-detail',
    )
    author = serializers.ReadOnlyField(source='author.username')

    class Meta: 
        model = Wallet
        fields = (
            'url', 
            'pk',
            'name',
            'amount',
            'author',
            'transactions', 
            'created_at',
            'updated_at',
        )

class TransactionTagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'url',
            'name'
        )

class KindOfTransactionSerializer(serializers.HyperlinkedModelSerializer): 
    transactions = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='transaction-detail'
    )

    class Meta:
        model = KindOfTransaction
        fields = (
            'url',
            'pk',
            'name',
            'transactions',
            'created_at',
            'updated_at',
        )

class TagSerializer(serializers.HyperlinkedModelSerializer): 
    transactions = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True, 
        view_name='transaction-detail'
    )

    class Meta:
        model = Tag
        fields = (
            'url', 
            'pk',
            'name', 
            'transactions', 
            'created_at', 
            'updated_at',
        ) 

class TransactionSerializer(serializers.HyperlinkedModelSerializer): 
    # display the category name 
    wallet = serializers.SlugRelatedField(queryset=Wallet.objects.all(), slug_field='name')
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='name')
    kind = serializers.SlugRelatedField(queryset=KindOfTransaction.objects.all(), slug_field='name')
    author = serializers.ReadOnlyField(source='author.username')
    tags = TransactionTagSerializer(many=True, required=False)
    class Meta:
        model = Transaction
        fields = (
            'url',
            'pk',
            'wallet',
            'category',
            'author',
            'kind',
            'tags',
            'name',
            'amount',
            'description',
            'created_at',
            'updated_at',
        )
    
    # this method for modify data before validation step
    def to_internal_value(self, data):
        try:
            tags_data = data['tags']
        except:
            tags_data = []
        finally:
            tags = []
            for tag_data in tags_data:
                tag = {'name': tag_data}
                tags.append(tag)
            data['tags'] = tags
            return super().to_internal_value(data)

    @staticmethod
    def add_tags_to_transaction(obj, tags_data):
        for tag_data in tags_data: 
            if len(Tag.objects.all().filter(name=tag_data['name'])) > 0:
                tag = Tag.objects.all().filter(name=tag_data['name'])[0]
                tag.transactions.add(obj)
            else: 
                tag = Tag.objects.create(name=tag_data['name'])
                tag.transactions.add(obj)

    def create(self, validated_data):
        try:
            tags_data = validated_data.pop('tags')
        except:
            tags_data = []
        finally:
            transaction = Transaction.objects.create(**validated_data)
            self.add_tags_to_transaction(transaction, tags_data)
            return transaction

    def update(self, instance, validated_data):
        try:
            tags_data = validated_data.pop('tags')
        except: 
            tags_data = []
        finally:
            instance.name = validated_data.get('title', instance.name)
            instance.description = validated_data.get('description', instance.content)
            instance.category = validated_data.get('category', instance.category)
            instance.author = validated_data.get('author', instance.author)
            self.add_tags_to_transaction(instance, tags_data)
            instance.save()
            return instance 

