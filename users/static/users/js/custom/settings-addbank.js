$('body').on('click', '.addbank-confirm-otp', function () {
    confirm_otp(function () {
        add_new_bank()
    })
})

$('.addbank-confirm').click(function () {
    let isEmpty = false;
    let ee = ''
    $('#add-bank-form input').each(function () {
        if ($(this).val().trim() === '' && $(this).attr('name') !== 'name') {
            isEmpty = true;
            ee = $(this).attr('name')
        }
    });
    if (!isEmpty) {
        confirm('Are you sure you want to add this account?', function () {
            launch_otp('addbank-confirm-otp')
            $('#addBankModal').modal('hide')
        })
    } else {
        console.log(`${ee} is empty`)
    }
})

function add_new_bank() {
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

function fetch_banks() {
    $.ajax({
        url: settings_base_url,
        type: 'POST',
        dataType: 'json',
        data: { 'action': 'fetch_banks' },
        success: function (data) {
            hidePreloader()
            if (data.status === "success") {
                $('#add-bank-bank').html('')
                $.each(data.banks, (index, bank) => {
                    $('#add-bank-bank').append(`<option value='${bank.bankCode}'>${bank['bankName']}</option>`)
                })
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