from decimal import Decimal

from payments import PurchasedItem
from payments.models import BasePayment

class Payment(BasePayment):

    def get_failure_url(self):
        return '../../payment/failure/'

    def get_success_url(self):
        return '../../payment/success/'
