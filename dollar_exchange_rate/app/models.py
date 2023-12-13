from django.db import models

# Create your models here.
class ExchangeRate(models.Model):
    rate_at = models.DateField(null=False, db_index=True, unique=True)
    brl = models.FloatField(null=False)
    eur = models.FloatField(null=False)
    jpy = models.FloatField(null=False)
    created_at = models.DateTimeField(null=False)

    def __str__(self):
        return f'{self.rate_at} {self.brl} {self.eur}'  