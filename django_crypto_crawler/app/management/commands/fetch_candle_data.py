
import requests
from datetime import datetime, timezone
from datetime import datetime
from django.core.management.base import BaseCommand
from app.models import Product, HistoricalData

class Command(BaseCommand):
    help = 'Fetch candle data from Coinbase API and store in database'

    def handle(self, *args, **options):
        products = Product.objects.all()
        for product in products:
            ticker = product.ticker
            self.fetch_and_store_data(ticker, product)
            print("Task DONE")

    def fetch_and_store_data(self, ticker, product):
        url = f"https://api.exchange.coinbase.com/products/{ticker}/candles"
        params = {
            'granularity': 60  # Daily candles
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            candles = response.json()
            for candle in candles:
                timestamp = datetime.fromtimestamp(candle[0], tz=timezone.utc)  # Create a timezone-aware datetime object
    
                open_price = candle[1]
                high_price = candle[2]
                low_price = candle[3]
                close_price = candle[4]
                HistoricalData.objects.update_or_create(
                    product=product,
                    timestamp=timestamp,
                    defaults={
                        'open': open_price,
                        'high': high_price,
                        'low': low_price,
                        'close': close_price
                    }
                )
        else:
            self.stdout.write(self.style.ERROR(f'Failed to fetch data for {ticker}'))
