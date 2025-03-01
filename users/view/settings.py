from django.views import View
from users.forms import NewBankForm, SettingsForm
from users.models import UserBankAccount, Notification
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
import re
from payment_utils.nuban import Nuban


class SettingsView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.form = None

    def post(self, request):
        self.user = request.user
        settings_form = SettingsForm(request.POST)
        if settings_form.is_valid():
            self.form = settings_form
            action = settings_form.cleaned_data.get("action")
            if action == "add_new_bank":
                return self.add_new_bank(request)
            elif action == "avatar":
                return self.update_avatar()
            elif action == "trash_bank":
                return self.delete_bank()
            elif action == "update_password":
                return self.update_password()
            elif action == "fetch_banks":
                return self.fetch_banks()
        print(settings_form.errors)
        return JsonResponse(
            {
                "status": "error",
                "message": "Invalid Action",
                "errors": settings_form.errors,
            }
        )

    def add_new_bank(self, request):
        form = NewBankForm(request.POST)
        nuban = Nuban()
        if form.is_valid():
            name_enq, name = nuban.name_enquiry(
                number=form.cleaned_data["number"], bank_code=form.cleaned_data["bank"]
            )
            if name_enq:
                if self.user.user_bank_accounts.count() < 3:
                    if len(name.split(" ")) >= 2:
                        matches = SettingsView.find_matches(
                            f"{self.user.first_name} {self.user.last_name}",
                            name
                        )
                        if matches > 0:
                            bank = nuban.get_bank_name(form.cleaned_data["bank"])
                            UserBankAccount.objects.create(
                                user=self.user,
                                bank_code=form.cleaned_data["bank"],
                                bank=bank,
                                number=form.cleaned_data["number"],
                                name=name,
                            )
                            return JsonResponse(
                                {
                                    "status": "success",
                                    "message": "Account added successfully",
                                }
                            )
                        return JsonResponse(
                            {
                                "status": "error",
                                "message": "Name does not match name on profile",
                            }
                        )
                    return JsonResponse(
                        {"status": "error", "message": "Please enter your full name"}
                    )
                return JsonResponse(
                    {"status": "error", "message": "You can only add up to 3 accounts"}
                )
            return JsonResponse(
                {"status": "error", "message": "Name enqury failed"}
            )
        return JsonResponse(
            {"status": "error", "message": "Please attend to all fields"}
        )

    def delete_bank(self):
        bank_id = int(self.form.cleaned_data.get("value"))
        bank = UserBankAccount.objects.filter(pk=bank_id)
        if bank:
            bank.delete()
            return JsonResponse({"status": "success", "message": "Success"})
        return JsonResponse({"status": "error", "message": "Bank does not exist"})

    def update_password(self):
        current_pass = self.form.cleaned_data.get("current_pass")
        new_pass = self.form.cleaned_data.get("new_pass")
        if check_password(current_pass, self.user.password):
            if re.match(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\.-_!\$%\(\)\=\+#]).{6,20}$",
                new_pass,
            ):
                self.user.set_password(new_pass)
                self.user.save()
                Notification.objects.create(
                    user=self.user,
                    title="Password Change",
                    body="Your account password was changed. If you did not authorize this, please quickly let us know",
                )
                return JsonResponse({"status": "success", "message": "Success"})
            return JsonResponse(
                {
                    "status": "error",
                    "message": "New password must contain at least 1 uppercase, 1 lowercase, 1 digit, and 1 special character",
                }
            )
        return JsonResponse(
            {"status": "error", "message": "Current Password does not match"}
        )

    def update_avatar(self):
        new_avatar_id = int(self.form.cleaned_data.get("value"))
        if new_avatar_id and 0 < new_avatar_id <= 28:
            self.user.avatar_id = new_avatar_id
            self.user.save()
            return JsonResponse({"status": "success", "message": "Success"})
        return JsonResponse({"status": "error", "message": "Invalid value"})
    
    def fetch_banks(self):
        nuban = Nuban()
        return JsonResponse({"status": "success", "banks": nuban.fetch_banks()})

    @staticmethod
    def find_matches(input1, input2):
        input1_list, input2_list = input1.lower().split(" "), input2.lower().split(" ")
        matches = 0
        for word in input1_list:
            if word in input2_list:
                matches += 1
        return matches
