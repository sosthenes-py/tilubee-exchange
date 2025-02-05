from django.views import View
from users.forms import NewBankForm, SettingsForm
from users.models import UserBankAccount
from django.http import JsonResponse


class SettingsView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def post(self, request):
        self.user = request.user
        settings_form = SettingsForm(request.POST)
        if settings_form.is_valid():
            action = settings_form.cleaned_data.get('action')
            if action == 'add_new_bank':
                return self.add_new_bank(request)
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid Action',
            'errors': settings_form.errors
        })
    
    def add_new_bank(self, request):
        form = NewBankForm(request.POST)
        if form.is_valid():
            if self.user.user_bank_accounts.count() < 3:
                if len(form.cleaned_data['name'].split(' ')) >= 2:
                    matches = SettingsView.find_matches(f'{self.user.first_name} {self.user.last_name}', form.cleaned_data['name'])
                    if matches > 0:
                        UserBankAccount.objects.create(user=self.user, bank=form.cleaned_data['bank'], number=form.cleaned_data['number'], name=f'{self.user.last_name} {self.user.first_name}')
                        return JsonResponse({
                            'status': 'success',
                            'message': 'Account added successfully'
                        })
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Name does not match name on profile'
                    })
                return JsonResponse({
                    'status': 'error',
                    'message': 'Please enter your full name'
                })
            return JsonResponse({
                'status': 'error',
                'message': 'You can only add up to 3 accounts'
                })
        return JsonResponse({
            'status': 'error',
            'message': 'Please attend to all fields'
                })
    
    @staticmethod
    def find_matches(input1, input2):
        input1_list, input2_list = input1.lower().split(' '), input2.lower().split(' ')
        matches = 0
        for word in input1_list:
            if word in input2_list:
                matches += 1
        return matches
