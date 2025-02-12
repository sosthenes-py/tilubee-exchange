from django import forms
from transactions.view.crypto import coins_dict


class DepositForm(forms.Form):
    action = forms.ChoiceField(required=True, choices=[
        ('bank', 'Bank Transfer'), ('uid', 'UID'), ('crypto', 'Crypto'),
        ('retrieve_bank_account', 'Retrieve Bank Account'), ('retrieve_crypto_wallet', 'Retrieve Crypto Wallet'), ('retrieve_uid', 'Retrieve UID')
    ])
    currency = forms.CharField(required=False, max_length=10, empty_value=None)
    qty = forms.FloatField(required=False)
    platform = forms.CharField(max_length=10, required=False, empty_value=None)
    ref = forms.CharField(max_length=10, required=False, empty_value=None)
    uid = forms.CharField(max_length=10, required=False, empty_value=None)
    wallet = forms.CharField(max_length=70, required=False, empty_value=None)


class WithdrawalForm(forms.Form):
    action = forms.ChoiceField(required=True, choices=[
        ('bank', 'Bank Transfer'), ('uid', 'UID'), ('crypto', 'Crypto'),
        ('retrieve_bank', 'Retrieve Bank Account')
    ])
    currency = forms.CharField(required=False, max_length=10, empty_value=None)
    amount = forms.FloatField(required=False)
    platform = forms.CharField(max_length=10, required=False, empty_value=None)
    wallet = forms.CharField(max_length=70, required=False, empty_value=None)
    bank_id = forms.IntegerField(required=False)


class NewBankForm(forms.Form):
    number = forms.CharField(max_length=20)
    bank = forms.CharField(max_length=20)
    name = forms.CharField(max_length=50)


class SettingsForm(forms.Form):
    action = forms.ChoiceField(choices=[
        ('add_new_bank', 'add New Bank'),
    ])


class ConvertQuoteForm(forms.Form):
    action2 = forms.ChoiceField(choices=[
        ('quote', 'Quote'),
        ('confirm', 'Confirm')
    ], required=True)
    from_qty = forms.FloatField(required=True)
    from_coin = forms.ChoiceField(choices=[
        (coin, full)
        for coin, full in coins_dict.items()
    ], required=True)
    to_coin = forms.ChoiceField(choices=[
        (coin, full)
        for coin, full in coins_dict.items()
    ], required=True)


class FilterForm(forms.Form):
    action = forms.ChoiceField(choices=[
        ('filter', 'Filter')
    ], required=True)
    category = forms.ChoiceField(choices=[
        ('all', 'All'),
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal')
    ], required=True)
    duration = forms.ChoiceField(choices=[
        (0, 'All'),
        (1, '24 hours'),
        (7, '7 days'),
        (12, '12 days'),
        (30, '30 days'),
        (90, '90 days'),
        (180, '180 days'),
        (360, '360 days')
    ], required=True)





