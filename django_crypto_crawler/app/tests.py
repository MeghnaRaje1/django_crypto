from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Product, HistoricalData

class ProductCRUDTestCase(TestCase):
    def setUp(self):
        self.product_data = [
            {"ticker": "BTC-USD", "name": "Bitcoin"},
            {"ticker": "ETH-USD", "name": "Ethereum"},
            {"ticker": "ADA-USD", "name": "Cardano"},
            {"ticker": "SOL-USD", "name": "Solana"},
        ]

    def test_create_product(self):
        for data in self.product_data:
            Product.objects.create(**data)
        self.assertEqual(Product.objects.count(), len(self.product_data))

    def test_read_product(self):
        for data in self.product_data:
            Product.objects.create(**data)
        products = Product.objects.all()
        self.assertEqual(len(products), len(self.product_data))
        for product, data in zip(products, self.product_data):
            self.assertEqual(product.ticker, data["ticker"])
            self.assertEqual(product.name, data["name"])

    def test_update_product(self):
        product = Product.objects.create(**self.product_data[0])
        new_name = "Bitcoin Revised"
        product.name = new_name
        product.save()
        updated_product = Product.objects.get(pk=product.id)
        self.assertEqual(updated_product.name, new_name)

    def test_delete_product(self):
        product = Product.objects.create(**self.product_data[0])
        product.delete()
        self.assertEqual(Product.objects.count(), 0)

    def test_empty_database(self):
        self.assertEqual(Product.objects.count(), 0)
        self.assertEqual(HistoricalData.objects.count(), 0)


    def test_retrieve_data_by_ticker(self):
        ticker = "BTC-USD"
        product = Product.objects.create(ticker=ticker, name="Bitcoin")
        HistoricalData.objects.create(product=product, timestamp="2024-01-14 15:25", open=12.01, high=12.56, low=11.8, close=12.45)
        retrieved_data = HistoricalData.objects.filter(product__ticker=ticker)
        self.assertEqual(retrieved_data.count(), 1)
        self.assertEqual(retrieved_data[0].product.ticker, ticker)

    def test_update_data_by_ticker(self):
        ticker = "BTC-USD"
        product = Product.objects.create(ticker=ticker, name="Bitcoin")
        historical_data = HistoricalData.objects.create(product=product, timestamp="2024-01-14 15:25", open=12.01, high=12.56, low=11.8, close=12.45)
        new_open_price = 12.5
        historical_data.open = new_open_price
        historical_data.save()
        updated_data = HistoricalData.objects.get(pk=historical_data.pk)
        self.assertEqual(updated_data.open, new_open_price)

    def test_delete_data_by_ticker(self):
        ticker = "BTC-USD"
        product = Product.objects.create(ticker=ticker, name="Bitcoin")
        historical_data = HistoricalData.objects.create(product=product, timestamp="2024-01-14 15:25", open=12.01, high=12.56, low=11.8, close=12.45)
        historical_data.delete()
        self.assertEqual(HistoricalData.objects.filter(product__ticker=ticker).count(), 0)

    def test_data_integrity(self):
        ticker = "BTC-USD"
        product = Product.objects.create(ticker=ticker, name="Bitcoin")
        HistoricalData.objects.create(product=product, timestamp="2024-01-14 15:25", open=12.01, high=12.56, low=11.8, close=12.45)
        product.delete()
        self.assertEqual(HistoricalData.objects.filter(product__ticker=ticker).count(), 0)
