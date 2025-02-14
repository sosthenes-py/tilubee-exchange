     $('body').on('click', '.addbank-confirm-otp', function(){
            confirm_otp(function(){
                add_new_bank()
            })
        })

        $('.addbank-confirm').click(function(){
            let isEmpty = false;
            $('#add-bank-form input').each(function() {
                if ($(this).val().trim() === '') {
                    isEmpty = true;
                }
            });
            if(!isEmpty){
                confirm('Are you sure you want to add this account?', function(){
                    launch_otp('addbank-confirm-otp')
                    $('#addBankModal').modal('hide')
                })
            }
        })

        function add_new_bank(){
            let myForm = $('#add-bank-form').serialize();
            myForm += '&action=add_new_bank';
            showPreloader()
            $.ajax({
                url: settings_base_url,
                type: 'POST',
                dataType: 'json',
                data: myForm,
                success: function (data) {
                    hidePreloader()
                    if (data.status === "success") {
                        $('#addBankModal').modal('hide')
                        notify(data.status, data.message, null, wallet_base_url)
                    } else {
                        $('#addBankModal').modal('show')
                        notify(data.status, data.message)
                    }
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    hidePreloader()
                    notify('error', xhr.status + ': ' + xhr.statusText)
                },
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", csrf_token)
                }
            })
        }