$(function(){
    for(let i=1; i <= 28; i++){
        $('.avatar-list').append(`
            <li>
                    <a href="#0" class="tf-list-item d-flex flex-column gap-4 align-items-center avatar-select" data-value="${i}">
                        <img src="${images_base_url}/avt/avt${i}.jpg" alt="img" class="box-round">
                        <p class="text-center"></p>
                    </a>
                </li>
        `)
    }

    window.myForm = {}
})

$('.logout').click(function(){
    confirm('Are you sure you want to logout?', function(){
        window.location.href=logout_url
    })
})


$('body').on('click', '.avatar-select', function(){
    window.myForm['action'] = 'avatar'
    window.myForm['value'] = $(this).data('value')
    confirm('Continue to update your profile avatar?', function(){
        function success(){
            info('Avatar updated successfully')
            $('#avatarModal').modal('hide')
            $('.user-avatar').attr('src', `${images_base_url}/avt/avt${window.myForm['value']}.jpg`)
        }
        function error(){
            info('An error occurred while trying to update avatar')
            $('avatarModal').modal('hide')
        }
        submit({s: success, e: error})
    })
})

$('.view-banks').click(function(){
    window.myForm = {}
    populate_banks()
    overlay_modal('viewBankModal')
})

function populate_banks() {
    $('.banks-list').html('')
    $.each(window.user_banks, function (index, details) {
        $('.banks-list').append(
            `<li ><div class="d-flex justify-content-between align-items-center gap-8 text-large item-check"
                 >${details.number} (${details.bank}) <i class="icon icon-cancel bank-trash" style="display: block"
                 data-bank_id="${details.id}"
                 data-name="${details.number} (${details.bank})"
                 ></i> </div></li>`
        )
    })
}

$('body').on('click', '.bank-trash', function(){
    const bank_id = $(this).data('bank_id')
    const name = $(this).data('name')
    window.myForm = {'action': 'trash_bank', 'value': bank_id}
    confirm(`The bank ${name} will be dissociated from your account`, function(){
        $('#viewBankModal').modal('hide')
        function success(){
            info('Bank has been deleted', 2, false)
            //Remove the deleted bank from the list in window
            $.each(window.user_banks, function(index, details){
                if(details.id === bank_id){
                    window.user_banks.splice(index, 1)
                }
            })
        }
        function error(){
            info('An error occurred please try again later')
            $('viewBankModal').modal('hide')
        }
        submit({s: success, e: error})
    })
})

$('.update-password').click(function(){
    event.preventDefault()
    let current_pass = $("#current_pass").val()
    let new_pass = $("#new_pass").val()
    if(current_pass !== '' && new_pass !== ''){
        window.myForm = {'action': 'update_password', 'current_pass': current_pass, 'new_pass': new_pass}
        confirm(`Proceed to change your account password`, function(){
            $('#viewBankModal').modal('hide')
            function success(){
                info('Password updated successfully', 2, false)
                $('#passwordModal').modal('hide')
            }
            
            submit({s: success})
        })
    }
})

function submit({s, e} = {}){
    showPreloader()
    $.ajax({
        url: settings_base_url,
        type: 'POST',
        dataType: 'json',
        data: window.myForm,
        success: function (data) {
            hidePreloader()
            if (data.status === "success" && typeof s === 'function') {
                s()
            }else if(data.status === "error" && typeof e === 'function'){
                e()
            }else if(data.status !== "success"){
                notify('error', data.message)
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