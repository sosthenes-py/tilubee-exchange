from django.views import View
from transactions.models import Transaction, Conversion
from transactions.view.crypto import coins_dict, bcdiv
from django.db.models import Count, QuerySet
from typing import Optional


class UserTransactions:
    """
    Return all transactions made by user in a list of dictionaries
    """
    def __init__(self, user=None, one_usd_in_base=None, base_currency=None, query: Optional[QuerySet]=None):
        self.user = user
        self.one_usd_in_base = one_usd_in_base
        self.base_currency = base_currency
        self.query = query

    def as_list(self):
        transactions = Transaction.objects.filter(user=self.user).order_by('-created_at')
        history = [
            {
                'type': transaction.transaction_type,
                'status': transaction.status,
                'qty': bcdiv(transaction.qty),
                'fee': transaction.fee,
                'in_base': f'{bcdiv(transaction.qty, self.one_usd_in_base)} {self.base_currency}',
                'currency': transaction.currency,
                'created_at': f'{transaction.created_at:%Y-%m-%d %H:%M:%S}',
                'updated_at': transaction.updated_at if not transaction.updated_at else f'{transaction.updated_at:%Y-%m-%d %H:%M:%S}',
                'address': transaction.address,
                'reference': transaction.reference,
                'hash': transaction.hash,
                'currency_name': coins_dict.get(transaction.currency, "NULL"),
                'medium': transaction.medium
            }
            for transaction in transactions
        ]
        return history

    def favorites(self):
        """
        Returns most frequently used currencies according to transactions
        """
        transactions = Transaction.objects.filter(user=self.user).values('currency').annotate(count=Count('id')).order_by('-count')
        return transactions

    def get_conversions(self):
        if self.query:
            conversions = self.query.order_by('-created_at')
        else:
            conversions = Conversion.objects.filter(user=self.user).order_by('-created_at')
        history = [
            {
                'status': tx.status,
                'qty_from': bcdiv(tx.qty_from),
                'qty_to': bcdiv(tx.qty_to),
                'currency_from': tx.currency_from,
                'currency_to': tx.currency_to,
                'created_at': f'{tx.created_at:%Y-%m-%d %H:%M:%S}',
            }
            for tx in conversions
        ]
        return history
