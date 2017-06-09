from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone

from django.core.validators import MinValueValidator
from decimal import Decimal

from payments import PurchasedItem
from payments.models import BasePayment


class Prices(models.Model):
    premium = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], default=Decimal(0))

class Premium(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    date_fin = models.DateField()

class Payment(BasePayment):

    def get_failure_url(self):
        return '../../payment/failure/'

    def get_success_url(self):
        return '../../payment/success/'

class PaymentLink(models.Model):
    premium = models.ForeignKey(Premium, on_delete=models.CASCADE, null=True)
    atelier = models.ForeignKey('atelier.inscription_log',
            on_delete=models.CASCADE, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    user = models.ForeignKey(
            'auth.User', on_delete=models.CASCADE,
            related_name='payments_log'
    )
