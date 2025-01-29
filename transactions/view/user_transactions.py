from django.views import View
from transactions.models import Transaction, Conversion
from transactions.view.crypto import coins_dict, bcdiv
from django.db.models import Count


class UserTransactions:
    """
    Return all transactions made by user in a list of dictionaries
    """
    def __init__(self, user, one_usd_in_base, base_currency):
        self.user = user
        self.one_usd_in_base = one_usd_in_base
        self.base_currency = base_currency

    def as_list(self):
        transactions = Transaction.objects.filter(user=self.user).order_by('created_at')
        history = [
            {
                'type': transaction.transaction_type,
                'status': transaction.status,
                'amount': bcdiv(transaction.amount),
                'in_base': f'{bcdiv(transaction.amount, self.one_usd_in_base)} {self.base_currency}',
                'currency': transaction.currency,
                'created_at': transaction.created_at,
                'updated_at': transaction.updated_at,
                'address': transaction.address,
                'reference': transaction.reference,
                'hash': transaction.hash,
                'currency_name': coins_dict.get(transaction.currency, "NULL"),
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
        conversions = Conversion.objects.filter(user=self.user).order_by('created_at')
        history = [
            {
                'status': tx.status,
                'amount_from': bcdiv(tx.amount_from),
                'amount_to': bcdiv(tx.amount_to),
                'currency_from': bcdiv(tx.currency_to),
                'created_at': tx.created_at,
            }
            for tx in conversions
        ]
        return history
