class Nuban:
    def generate_virtual_account(self, user):
        return {
            'status': 'success',
            'data': {
                'account_number': '123456789',
                'bank_name': 'Dummy Bank'
            }
        }