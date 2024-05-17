from django.db import models

class Product(models.Model):
    ticker = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class HistoricalData(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()

    def __str__(self):
        return f"{self.product.name} - {self.timestamp}"
