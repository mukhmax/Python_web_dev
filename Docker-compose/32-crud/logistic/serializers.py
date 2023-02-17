from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price', ]


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for position in positions:
            StockProduct.objects.create(stock_id=stock.id,
                                        product_id=position['product'].id,
                                        quantity=position['quantity'],
                                        price=position['price'])
        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for position in positions:
            if position['product'].id not in [pos.product_id for pos in instance.positions.all()]:
                StockProduct.objects.create(stock_id=instance.id,
                                            product_id=position['product'].id,
                                            quantity=position['quantity'],
                                            price=position['price'])
            else:
                instance.positions.filter(product_id=position['product'].id).update(stock_id=instance.id,
                                                                                    product_id=position['product'].id,
                                                                                    quantity=position['quantity'],
                                                                                    price=position['price'])
        return stock
