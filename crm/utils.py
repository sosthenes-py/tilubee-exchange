import re
import django.db.models
from django.utils import timezone
import datetime as dt
from django.db.models import (
    Sum,
    Count,
    Case,
    When,
    Value,
    F,
    DecimalField,
    Q,
    OuterRef,
    Subquery,
    IntegerField,
    FloatField,
)
from django.db.models.functions import TruncDay, TruncMonth, Coalesce, Lower
from payment_utils.tickers import COINS_DICT, markets as crypto_markets
from payment_utils.funcs import bcdiv
from crm.models import AdminUser, AdminLog, Note
from users.models import AppUser, VirtualAccount, UserWallet, Notification
from users.nuban import Nuban
from transactions.models import Transaction, Asset
from django.contrib.auth.hashers import make_password, check_password
import json
from django.conf import settings
from crm.models import Blacklist
from django.db import transaction
import random
from string import digits

nuban = Nuban()


class Func:
    @staticmethod
    def format_agent_id(num: int):
        if num < 10:
            return f"00{num}"
        else:
            return f"0{num}"

    @staticmethod
    def generate_txid(id):
        length = 9 - len(str(id))
        suffix = "".join([random.choice(digits) for _ in range(length)])
        return f"{id}{suffix}"

    @staticmethod
    def update_transaction(tx: Transaction, status: str, qty: float | None = None):
        """
        Update Transactions. This method updates user balance when successful
        """
        if qty is not None:
            tx.qty = qty
            tx.amount_usd = crypto_markets()[tx.currency]["price"] * qty

        # FOR DEPOSIT
        if tx.transaction_type == "deposit":
            if status in ("completed", "failed") and tx.medium in ("uid", "bank"):
                if status == "completed":
                    tx.status = "completed"
                    bal = getattr(tx.user.assets, tx.currency)
                    setattr(tx.user.assets, tx.currency, bal + tx.qty)
                    note = f"Deposit of {bcdiv(tx.qty):,} {tx.currency.upper()} has been confirmed"
                elif status == "failed":
                    tx.status = "failed"
                    note = f"Unfortunately, your deposit of {bcdiv(tx.qty):,} {tx.currency.upper()} failed"
                tx.user.assets.save()
                tx.save()
                Notification.objects.create(
                    user=tx.user,
                    title=f"Deposit {status.title()}",
                    body=note,
                )
                return True
            return False

        # FOR WITHDRAWAL
        elif tx.transaction_type == "withdrawal":
            if status in ("completed", "failed") and tx.medium in (
                "uid",
                "bank",
                "crypto",
            ):
                if status == "completed":
                    tx.status = "completed"
                    if tx.medium == "uid":
                        # Nothing to do
                        pass
                    elif tx.medium == "bank":
                        # Complete bank withdrawal
                        pass
                    elif tx.medium == "crypto":
                        # Complete crypto withdrawal
                        pass
                    note = f"Withdrawal of {bcdiv(tx.qty):,} {tx.currency.upper()} has been completed"
                elif status == "failed":
                    bal = getattr(tx.user.assets, tx.currency)
                    setattr(tx.user.assets, tx.currency, bal + tx.qty)
                    tx.status = "failed"
                    note = f"Unfortunately, your withdrawal of {bcdiv(tx.qty):,} {tx.currency.upper()} failed. Asset has been returned to your wallet."
                tx.user.assets.save()
                tx.save()
                Notification.objects.create(
                    user=tx.user,
                    title=f"Deposit {status.title()}",
                    body=note,
                )
                return True
            return False

    @staticmethod
    def create_virtual_account(user: AppUser):
        # After creating virtual account, store to db
        res = nuban.generate_virtual_account(user)
        if res["status"] == "success":
            bank_number = res["data"]["account_number"]
            bank_name = res["data"]["bank_name"]
            bank_code = 0
            tx_ref = ""
        else:
            bank_number = "1234567890"
            bank_name = "Dummy Bank"
            bank_code = 0
            tx_ref = ""
        VirtualAccount(
            user=user, number=bank_number, bank=bank_name, name=tx_ref
        ).save()


class UserUtils:
    def __init__(self, request, **kwargs):
        self.user, self.users, self.uid, self._content, self._content2 = (
            None,
            None,
            None,
            None,
            None,
        )
        self.avatar = ""
        self.kwargs = kwargs
        self.action = self.kwargs["action"]
        self.request = request
        self._status, self._message = "success", "success"

    def fetch_users_in_table(
        self,
        rows=10,
        start=f"{dt.date.today() - dt.timedelta(days=60):%Y-%m-%d}",
        end=f"{dt.date.today():%Y-%m-%d}",
        filters="",
    ):
        start_date = dt.datetime.strptime(start, "%Y-%m-%d")
        start_date = timezone.make_aware(start_date, timezone.get_current_timezone())

        end_date = dt.datetime.strptime(end, "%Y-%m-%d") + dt.timedelta(days=1)
        end_date = timezone.make_aware(end_date, timezone.get_current_timezone())

        users = (
            AppUser.objects.annotate(
                first_name_lower=Lower("first_name"), last_name_lower=Lower("last_name")
            )
            .filter(
                (Q(created_at__gte=start_date) & Q(created_at__lte=end_date))
                & (
                    Q(uid__startswith=filters)
                    | Q(phone__startswith=filters)
                    | Q(first_name_lower__startswith=filters.lower())
                    | Q(last_name_lower__startswith=filters.lower())
                )
            )
            .order_by("-created_at")
            .all()
        )
        self._content = ""
        rows = int(rows)
        for user in users:
            if rows > 0:
                self.add_table_content(_for="all_users_table", user=user)
                rows -= 1

    def fetch_other_details(self):
        self._content = {}

        if self.user.virtual_accounts.exists():
            virtual_accounts = {
                "number": self.user.virtual_accounts.last().number,
                "name": self.user.virtual_accounts.last().name,
                "bank": self.user.virtual_accounts.last().bank,
            }
        else:
            virtual_accounts = {}
        banks = [
            {
                field.name: getattr(bank, field.name)
                for field in bank._meta.fields
                if field.name not in ("id", "user")
            }
            for bank in self.user.user_bank_accounts.all()
        ]
        assets = {
            field.name: getattr(self.user.assets, field.name)
            for field in self.user.assets._meta.fields
            if field.name not in ("id", "user")
        }
        wallets = list(
            self.user.user_wallets.values(
                "currency", "currency_name", "address", "network"
            )
        )

        self.fetch_notes_in_table()
        self._content["tables"] = {"notes": self._content2}

        self._content = {
            "virtual_accounts": virtual_accounts,
            "banks": banks,
            "notes": self._content2,
            "tx_count": self.user.transactions.count(),
            "notes_count": self.user.note_set.count(),
            "wallets": wallets,
            "assets": assets,
        }

    def fetch_notes_in_table(self):
        self._content2 = ""
        for note in self.user.note_set.all().order_by("-id"):
            modified = ""
            if note.modified:
                modified = f"📢 modified- {note.modified_at:%d/%m/%y}"
            self.add_table_content(_for="note", note=note, modified=modified)

    def delete_note(self):
        note = Note.objects.get(pk=self.kwargs["note_id"])
        if not note.super and self.request.user.level in [
            "super admin",
            "team leader",
            "admin",
        ]:
            action = f"Deleted note: ({note.body[:18]}...)"
            # AdminUtils.log(user=self.request.user, app_user=self.user, action_type='delete_note', action=action)
            note.delete()
            self._message = "Note deleted successfully"
        else:
            self._message = "Comment cannot be deleted"
            self._status = "info"
        self.fetch_notes_in_table()
        self._content = self._content2

    def add_note(self):
        note = Note(
            user=self.request.user,
            app_user=self.user,
            body=self.kwargs["note"],
            super=False,
        )
        note.save()
        self._message = "Note added successfully!"
        self.fetch_notes_in_table()
        self._content = self._content2

    def modify_note(self):
        note = Note.objects.get(pk=self.kwargs["note_id"])
        if note.body != self.kwargs["note"] and not note.super:
            action = f"Modified note: ({note.body[:15]}...)"
            # AdminUtils.log(user=self.request.user, app_user=self.user, action_type='add_note', action=action)
            note.body = self.kwargs["note"]
            note.modified_at = timezone.now()
            note.modified = True
            note.save()
            self._message = "Note modified successfully"
        else:
            self._message = "Nothing changed"
            self._status = "info"

    def update_user(self):
        if self.request.user.level in ("super admin", "admin", "approval admin"):
            amount_fields = ["eligible_amount"]
            key = self.kwargs["key"]
            value = self.kwargs["value"]
            if key in amount_fields:
                value = float(value.replace(",", ""))
            if value == getattr(self.user, key):
                self._message = "No changes was made"
                self._status = "info"
                return None
            if key == "borrow_level":
                value = int(value)
                if value < getattr(self.user, key):
                    self._message = "Account downgrade not allowed"
                    self._status = "error"
                    return None
                if value > getattr(self.user, key):
                    setattr(self.user, key, value)

            log_detail = (
                f"Updated user's {key} from {getattr(self.user, key)} to {value}"
            )

            setattr(self.user, key, value)
            self.user.save(using="default")
            # AdminUtils.log(self.request.user, app_user=self.user, action_type='profile update', action=log_detail)
            self._message = f"{key} updated successfully"
        else:
            self._message = "No permission"
            self._status = "error"
            return None

    def delete_user(self):
        self.user.delete()
        self._message = "User deleted successfully"
        self._status = "success"

    def doc_decide(self):
        if self.request.user.level in ("super admin", "admin"):
            if self.kwargs["doc_action"] == "approve":
                self.user.status = True
                status = "success"
            else:
                self.user.status = False
                self.user.status_reason = self.kwargs["doc_reason"]
                status = "danger"
            self.user.save()
            self._message = f'Docs {self.kwargs["doc_action"]}d for user'
            self._status = "success"
            self._content = f"""User Docs  <span class="badge text-bg-{status}">{self.kwargs['doc_action'].upper()}D</span>"""
        else:
            self._message = f"No such permission. Please contact admin"
            self._status = "danger"
            self._content = f"""User Docs  <span class="badge text-bg-{'success' if self.user.status else 'danger'}">STATUS</span>"""
        self._content = {
            "doc_status": self.user.status,
            "doc_reason": self.user.status_reason,
            "html": self._content,
        }

    def blacklist(self):
        if self.request.user.level in ("super admin"):
            action = self.kwargs["main_action"]
            if "Blacklist" in action:
                if not self.user.is_blacklisted():
                    Blacklist(user=self.user).save()
            else:
                self.user.blacklist.delete()
        else:
            self._message = f"No such permission. Please contact admin"
            self._status = "danger"

    def fetch_blacklist(
        self,
        rows=10,
        start=f"{dt.date.today() - dt.timedelta(days=60):%Y-%m-%d}",
        end=f"{dt.date.today():%Y-%m-%d}",
        filters="",
    ):
        start_date = dt.datetime.strptime(start, "%Y-%m-%d")
        start_date = timezone.make_aware(start_date, timezone.get_current_timezone())

        end_date = dt.datetime.strptime(end, "%Y-%m-%d") + dt.timedelta(days=1)
        end_date = timezone.make_aware(end_date, timezone.get_current_timezone())

        items = (
            Blacklist.objects.filter(
                (Q(created_at__gte=start_date) & Q(created_at__lte=end_date))
                & (
                    Q(user__uid__startswith=filters)
                    | Q(user__phone__startswith=filters)
                    | Q(user__email__startswith=filters)
                )
            )
            .order_by("-created_at")
            .all()
        )
        self._content = ""
        rows = int(rows)
        for item in items:
            if rows > 0:
                self.add_table_content(_for="blacklist", row=item)
                rows -= 1

    def process(self):
        if self.action == "get_all_users":
            self.fetch_users_in_table(
                rows=self.kwargs.get("rows", 10),
                start=self.kwargs.get("start"),
                end=self.kwargs.get("end"),
                filters=self.kwargs.get("filters"),
            )
        elif self.action == "fetch_blacklist":
            self.fetch_blacklist(
                rows=self.kwargs.get("rows", 10),
                start=self.kwargs.get("start"),
                end=self.kwargs.get("end"),
                filters=self.kwargs.get("filters"),
            )
        else:
            self.user = AppUser.objects.get(uid=self.kwargs["uid"])
            if self.action == "get_other_details":
                self.fetch_other_details()
            elif self.action == "update_user":
                self.update_user()
                self.content = self.message
            elif self.action == "delete_note":
                self.delete_note()
            elif self.action == "add_note":
                self.add_note()
            elif self.action == "modify_note":
                self.modify_note()
            elif self.action == "blacklist":
                self.blacklist()
            elif self.action == "doc_decide":
                self.doc_decide()
            elif self.action == "delete_user":
                self.delete_user()

    def add_table_content(self, _for="", **kwargs):
        if _for == "all_users_table":
            user = kwargs["user"]
            user_presence = "online" if not user.is_blacklisted() else "offline"
            self._content += f"""
                                <tr 
                                    data-first_name='{user.first_name}' 
                                    data-last_name='{user.last_name}' 
                                    data-phone='{user.phone}' 
                                    data-email='{user.email}' 
                                    data-created_at="{user.created_at:%a %b %d, %Y}" 
                                    data-avatar="/static/crm/images/avt/avt{user.avatar_id}.jpg" 
                                    
                                    data-status='{'Active' if not user.is_blacklisted() or hasattr(user, 'whitelist') else 'Blacklisted'}' 
                                    data-doc_status="{user.status}"
                                    data-doc_reason="{user.status_reason}"
                                    data-status_pill='<span class="badge rounded-pill text-bg-{'success' if not user.is_blacklisted() or hasattr(user, 'whitelist') else 'danger'}">{'Active' if not user.is_blacklisted() else f'Blacklisted: {getattr(user, "blacklist").created_at:%b %d}: {getattr(user, "blacklist").reason}'}</span>'
                                    data-uid='{user.uid}'
                                    class='user_rows' data-bs-toggle='modal' data-bs-target='#exampleLargeModal1'>

                                   

                                	<td>
                                	<div class="ms-2">
										<h6 class="mb-0 font-14 fw-bold">{user.uid}
										<span style="font-size: 8px" class="fw-bold text-primary"></span>
										</h6>
									</div>
                                	</td>
                                	<td>{user.last_name} {user.first_name}</td>
                                	<td>{user.phone}</td>
                                	<td>{user.email}</td>
                                	<td>{user.created_at:%a %b %d, %Y}</td>
                                	<td>{user.last_access:%a %b %d, %Y}</td>	
                                </tr>
                            """

        elif _for == "note":
            note = kwargs["note"]
            self._content2 += f"""
                        <div class="col-12">
                            <div id="todo-container">
                                    <div class="pb-3 todo-item">
                                        <div class="input-group">

                                            <div class="input-group-text">
                                                <input type="checkbox" aria-label="Checkbox for following text input" data-id="{note.id}" disabled class="task-status">
                                            </div>

                                            <textarea data-id="{note.id}" class="form-control old_note" rows=2>{note.body}</textarea>

                                            <button class="btn btn-outline-secondary bg-danger text-white delete_note" data-id="{note.id}" type="button">X</button>
                                            <div style="width: 100%; display: inine-block; background: #E9ECEF" >
                                            <span style="float: left; width: 40%" class="px-2"> By: S{note.user.stage}-{Func.format_agent_id(note.user.stage_id)}
                                            </span>
                                            <span style="float: right; width: 40%; text-align: right" class="px-2">-{note.created_at:%a %d %b, %Y @ %I:%M %p} <span style="font-weight: bold" class="text-primary">{kwargs['modified']}</span>
                                            </span>
                                            </div>

                                        </div>
                                </div>
                            </div>
                        </div>
                        """

        elif _for == "blacklist":
            row = kwargs["row"]
            user = row.user
            
            self._content += f"""
                <tr
                class='user_rows'
                >
                    <td>
						<div class="d-flex align-items-center">
							<div class="loan-checkbox-cont">
								<input class="form-check-input me-3 loan-checkbox border-primary border-2" type="checkbox" value="" aria-label="...">
							</div>
							<div class="ms-2">
								<h6 class="mb-0 font-14 fw-bold">{row.user.uid}</h6>
							</div>
						</div>
					</td>
                    <td>{row.user.uid}</td>
                    <td>{row.user.email}</td>
                    <td>{row.created_at:%a %b %d, %Y}</td>
                </tr>

            """

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    @property
    def content2(self):
        return self._content2

    @content2.setter
    def content2(self, value):
        self._content2 = value


class AdminUtils:
    def __init__(self, request, **kwargs):
        self.admin_user: AdminUser = request.user
        self.kwargs = kwargs
        self._status, self._message, self._content = "success", "success", None
        self.action = kwargs["action"]

    @staticmethod
    def log(user: AdminUser, app_user: AppUser, action_type="", action=""):
        AdminLog(
            user=user, app_user=app_user, action_type=action_type, action=action
        ).save()

    def fetch_operators(self):
        agents = AdminUser.objects.all().order_by("-created_at").all()

        sn = 0
        self._content = ""
        for agent in agents:
            sn += 1
            self.add_table_content(_for="operators", sn=sn, agent=agent)

    def modify_admin(self):
        admin = AdminUser.objects.get(pk=self.kwargs["uid"])
        admin.first_name = self.kwargs["first_name"]
        admin.last_name = self.kwargs["last_name"]
        admin.phone = self.kwargs["phone"]
        if self.kwargs["password"] != "":
            admin.password = make_password(self.kwargs["password"])
        admin.save()
        self._message = "Modified successfully"
        self._status = "success"

    def delete_operator(self):
        admin = AdminUser.objects.get(pk=self.kwargs["uid"])
        if self.admin_user.level in ["super admin", "admin"]:
            admin.delete()
            self._message = "Operator deleted successfully"
        else:
            self._message = "No such privilege"

    def add_table_content(self, _for="", **kwargs):
        if _for == "operators":
            agent = kwargs["agent"]
            sn = kwargs["sn"]
            if not agent.status:
                status_class = "danger"
                status_text = "Suspended"
            elif agent.level == "staff":
                if agent.status and agent.can_collect:
                    status_class = "success"
                    status_text = "Active, C-C"
                else:
                    status_class = "info"
                    status_text = "Active, N-C"
            else:
                status_class = "success"
                status_text = "Active"

            if agent.level == "super admin":
                level_class = "primary"
            elif agent.level == "admin":
                level_class = "secondary"
            elif agent.level == "approval admin":
                level_class = "warning"
            elif agent.level == "team leader":
                level_class = "info"
            else:
                level_class = "dark"

            stage = f"{agent.stage} - {Func.format_agent_id(agent.stage_id)}"
            if agent.level == "team leader":
                stage = f"TL - {agent.stage}.{agent.stage_id}"

            self._content += f"""
                <tr class='user_trs' 
                data-id='{agent.id}' 
                data-first_name='{agent.first_name}' 
                data-last_name="{agent.last_name}" 
                data-email='{agent.email}' 
                data-phone='{agent.phone}'
                data-level={agent.level}
                data-stage='{agent.stage}'
                data-created_at="{agent.created_at:%a %b %d, %Y}" 
                data-avatar="/static/crm/images/avatars/user.png" 
                data-status_pill='<span class="badge rounded-pill text-bg-{status_class}">{status_text}</span>' 
                data-bs-toggle='modal' data-bs-target='#operatorModal'>
				    <td>
				    {sn}
				    </td>
				    <td>{agent.first_name}</td>
				    <td>
					    <div class='badge rounded-pil w-50 text-bg-{level_class}'>{agent.level.title()}</div>
				    </td>
				    <td>
					    <div class='badge rounded-pill w-50 text-bg-dark'>{stage}</div>
				    </td>
				    <td>{agent.collection_set.count() if agent.level == 'staff' else '-'}</td>
				    <td>
					    <div class='badge rounded-pill w-50 text-bg-{status_class}'>{status_text}</div>
				    </td>
				    <td>{agent.last_login:%d %b, %H:%M}</td>	
			    </tr>
            """

    def process(self):
        if self.action == "fetch_operators":
            self.fetch_operators()
        elif self.action == "modify_account":
            self.modify_admin()
        elif self.action == "delete_operator":
            self.delete_operator()

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value


class TxUtils:
    def __init__(self, request, **kwargs):
        self.user, self.users, self.uid, self._content, self._content2, self.loan = (
            None,
            None,
            None,
            None,
            None,
            None,
        )
        self.kwargs = kwargs
        self.action = self.kwargs["action"]
        self.request = request
        self._status, self._message = "success", "success"

    def fetch_txs(
        self,
        size="single",
        rows=10,
        start=f"{dt.date.today() - dt.timedelta(days=60):%Y-%m-%d}",
        end=f"{dt.date.today():%Y-%m-%d}",
        filters="",
    ):
        if size != "single":
            start_date = dt.datetime.strptime(start, "%Y-%m-%d")
            start_date = timezone.make_aware(
                start_date, timezone.get_current_timezone()
            )

            end_date = dt.datetime.strptime(end, "%Y-%m-%d") + dt.timedelta(days=1)
            end_date = timezone.make_aware(end_date, timezone.get_current_timezone())

            txs = (
                Transaction.objects.annotate(
                    lower_first_name=Lower("user__first_name"),
                    lower_last_name=Lower("user__last_name"),
                )
                .filter(
                    Q(created_at__gte=start_date)
                    & Q(created_at__lte=end_date)
                    & (
                        Q(tx_id__startswith=filters)
                        | Q(medium__startswith=filters)
                        | Q(currency__startswith=filters)
                        | Q(user__uid__startswith=filters)
                        | Q(user__email__startswith=filters)
                        | Q(lower_first_name__startswith=filters.lower())
                        | Q(lower_last_name__startswith=filters.lower())
                    )
                )
                .order_by("-created_at")
                .all()
            )

            rows = int(rows)

            self._content = ""
            sn = 0
            for tx in txs:
                if self.request.user.level == "super admin":
                    if rows > 0:
                        self.add_table_content(
                            _for="txs", single=False, tx=tx, sn=sn, size=size
                        )

        else:
            self.user = AppUser.objects.get(uid=self.kwargs["uid"])
            # IF SIZE IS SINGLE
            txs = self.user.transactions.order_by("-created_at").all()
            self._content = ""
            sn = 0
            for tx in txs:
                sn += 1
                self.add_table_content(_for="txs", single=True, tx=tx, sn=sn, size=size)

    def status_update(self, to):
        qty = self.kwargs.get("qty", "single")
        if qty == "single":
            tx = Transaction.objects.get(pk=self.kwargs["tx_id"])
            self.user = AppUser.objects.get(uid=self.kwargs["uid"])
            if to == "completed":
                Func.update_transaction(tx, "completed")
            elif to == "failed":
                Func.update_transaction(tx, "failed")
            self._message = f"Transaction {to} successfully"
            self._status = "success"
            self.fetch_txs(size=self.kwargs["size"])
        else:
            pass

    def trash_tx(self):
        if self.request.user.level in ("super admin", "approval admin"):
            tx = Transaction.objects.get(pk=self.kwargs["tx_id"])
            tx.delete()
            # AdminUtils.log(user=self.request.user, app_user=loan.user, action_type='loan status',
            #                action=f'Deleted a loan with ID {loan.loan_id}')
            self._message = f"Tx request deleted successfully"
            self._status = "success"
            self.fetch_txs(size=self.kwargs["size"])
        else:
            self._message = f"Permission error"
            self._status = "error"

    def add_transaction(self):
        uuid = self.kwargs["uid"]
        user = AppUser.objects.filter(uid=uuid).first()
        if user:
            tx_type = self.kwargs["type"]
            currency = self.kwargs["currency"]
            qty = float(self.kwargs["qty"])
            medium = self.kwargs["medium"]
            amount_usd = crypto_markets()[currency]["price"] * qty

            wallet_balance = getattr(user.assets, currency)

            if tx_type == "deposit":
                wallet_balance += qty
            elif tx_type == "withdrawal":
                if wallet_balance >= qty:
                    wallet_balance -= qty
                else:
                    self._message = "Wallet balance too small for withdrawal"
                    self._status = "error"
                    return None
            setattr(user.assets, currency, wallet_balance)

            with transaction.atomic():
                tx = Transaction.objects.create(
                    user=user,
                    currency=currency,
                    qty=qty,
                    transaction_type=tx_type,
                    medium=medium,
                    amount_usd=amount_usd,
                )
                tx.tx_id = Func.generate_txid(tx.id)
                tx.save()

                action_word = "confirmed" if tx_type == "depsoit" else "completed"
                Notification.objects.create(
                    user=user,
                    title=f"Deposit {action_word.title()}",
                    body=f"Your deposit of {qty:,} {currency.upper()} has been {action_word}",
                )
                user.assets.save()

            self._message = (
                f"{tx_type.title()} of {qty} {currency.upper()} was successful"
            )
            self._status = "success"
            return None
        self._message = "User does not exist"
        self._status = "error"
        return None

    def load_coins(self):
        markets = crypto_markets()
        self._content = {
            short: {"long": long, "price": markets[short]["price"]}
            for short, long in COINS_DICT.items()
        }

    def add_table_content(self, _for="", **kwargs):
        if _for == "txs":
            tx = kwargs["tx"]
            if not kwargs["single"]:
                attach_user = f"{tx.user.email.split('@')[0]}"
            else:
                attach_user = ""

            avatar = f"/static/crm/images/avt/avt{tx.user.avatar_id}.jpg"

            status_text, status_class = "", ""
            if tx.status == "pending":
                status_class = "warning"
            elif tx.status == "completed":
                status_class = "success"
            else:
                status_class = "danger"

            self._content += f"""
                        <tr data-uid='{tx.user.uid}' 
                                    data-first_name='{tx.user.first_name}' 
                                    data-last_name='{tx.user.last_name}' 
                                    data-phone='{tx.user.phone}' 
                                    data-email='{tx.user.email}' 
                                    data-created_at="{tx.user.created_at:%a %b %d, %Y}" 
                                    data-avatar="{avatar}" 
                                    data-hash="{tx.hash}" 
                                    data-reference="{tx.reference}" 
                                    data-address="{tx.address}" 
                                    data-fee="{tx.fee}" 
                                    data-medium="{tx.medium}" 
                                    data-status='{'Active' if not tx.user.is_blacklisted() or hasattr(tx.user, 'whitelist') else 'Blacklisted'}' 
                                    data-doc_status="{tx.user.status}"
                                    data-doc_reason="{tx.user.status_reason}"
                                    data-status_pill='<span class="badge rounded-pill text-bg-{'success' if not tx.user.is_blacklisted() or hasattr(tx.user, 'whitelist') else 'danger'}">{'Active' if not tx.user.is_blacklisted() else f'Blacklisted: {getattr(tx.user, "blacklist").created_at:%b %d}: {getattr(tx.user, "blacklist").reason}'}</span>'
                                    data-style='grey' class='tx_rows'
                                    data-tx_id='{tx.tx_id}'
                                    data-bs-toggle='modal' data-bs-target='#exampleLargeModal1'
                                    >

                           <td>
								<div class="d-flex align-items-center">
									<div class="ms-2">
										<h6 class="mb-0 font-14 fw-bold">{tx.tx_id}
										<span style="font-size: 11px" class="fw-bold text-{'success' if tx.transaction_type == 'deposit' else 'danger'}">{tx.transaction_type[:3].title()}.</span>
										</h6>
										<p class="mb-0 font-13 text-{'danger' if tx.user.is_blacklisted() else 'secondary'}">{attach_user}</p>
									</div>
								</div>
							</td>
                			<td>{bcdiv(tx.qty):,} {tx.currency.upper()}</td>
                            <td>${bcdiv(tx.amount_usd):,}</td>
                            <td>{tx.medium.title()}</td>
                            <td>{tx.reference}</td>
                            <td><span class="copy" data-item="{tx.address}"><i class="bx bxs-copy font-18 me-1"></i> {'copy address' if tx.address == '' else 'None'}</span></td>
                            <td><span class="copy" data-item="{tx.hash}"><i class="bx bxs-copy font-18 me-1"></i> {'copy hash' if tx.hash == '' else 'None'}</span></td>
                            <td><span class="badge rounded text-bg-{status_class}">{tx.status}</span></td>
                			<td>{tx.created_at:%b %d, %Y}</td>"""
            if kwargs["size"] == "single":
                self._content += f"""
                			<td>
                				<div class='dropdown ms-auto'>
                				<div data-bs-toggle='dropdown' class='dropdown-toggle dropdown-toggle-nocaret cursor-pointer' aria-expanded='false'>
                				<i class='bx bx-dots-vertical-rounded font-22'></i>
                			</div>
                			<ul class='dropdown-menu' style='cursor: pointer;'>
                        """
                if self.request.user.level == "super admin":
                    if (
                        tx.status == "pending"
                        and tx.medium in ['bank', 'uid']
                        and tx.transaction_type == "deposit"
                    ):
                        self._content += f"""
                                        <li data-id='{tx.id}' data-uid='{tx.user.uid}' data-size='{kwargs["size"]}' data-action='completed' class='tx_actions bg-success'><a class='dropdown-item'><i class='bx bx-check font-22 '></i> Complete</a></li>
                                        
                                        <li data-id='{tx.id}' data-uid='{tx.user.uid}' data-size='{kwargs["size"]}' data-action='failed' class='tx_actions bg-danger'><a class='dropdown-item'><i class='bx bx-check font-22 '></i> Cancel</a></li>
                                        """
                    if tx.status == "pending" and tx.transaction_type == "withdrawal":
                        self._content += f"""
                                        <li data-id='{tx.id}' data-uid='{tx.user.uid}' data-size='{kwargs["size"]}' data-action='completed' class='tx_actions bg-success'><a class='dropdown-item'><i class='bx bx-check font-22 '></i> Complete</a></li>
                                        
                                        <li data-id='{tx.id}' data-uid='{tx.user.uid}' data-size='{kwargs["size"]}' data-action='failed' class='tx_actions bg-danger'><a class='dropdown-item'><i class='bx bx-check font-22 '></i> Cancel</a></li>
                                        """
                if self.request.user.level in ["super admin", "approval admin"]:
                    self._content += f"""
                    <li data-id='{tx.id}' data-uid='{tx.user.uid}' data-size='{kwargs["size"]}' data-action='trash_tx' class='tx_actions'><a class='dropdown-item'><i class='bx bx-trash font-22 '></i> Delete</a></li>
                    """
                self._content += f"""
                            </ul>
                        </div>
                    </td>
                """
            self._content += "</tr>"

    def process(self):
        if self.action == "fetch_all_txs":
            self.fetch_txs(
                size="multiple",
                rows=self.kwargs.get("rows", 10),
                start=self.kwargs.get("start"),
                end=self.kwargs.get("end"),
                filters=self.kwargs.get("filters"),
            )
        else:
            if self.action == "fetch_txs":
                self.fetch_txs(size="single")
            elif self.action == "status_update":
                if self.kwargs["main_action"] == "trash_tx":
                    self.trash_tx()
                else:
                    self.status_update(self.kwargs["main_action"])
            elif self.action == "add_tx":
                self.add_transaction()
            elif self.action == "load_coins":
                self.load_coins()

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    @property
    def content2(self):
        return self._content2

    @content2.setter
    def content2(self, value):
        self._content2 = value
