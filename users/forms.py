from django import forms


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