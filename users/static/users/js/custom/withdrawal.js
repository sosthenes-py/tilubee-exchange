
        function set_storage(action=null, key, value){
            if(action) {
                window.myForm['action'] = action
            }
            window.myForm[key] = value
        }

        function reset_storage(){
            $('.w-bank-conf').css('display', 'none')
            $('.w-notbank-wallet').css('display', 'none')
            window.myForm = {}
        }



        function w_populate_cryptos(){
            $('.cryptos-list').html('')
            $.each(window.wallets, function(coin, balance){
                if($.inArray(coin, main_wallets) !== -1 && coin !== 'ngn') {
                    $('.cryptos-list').append(
                        `<li data-bs-dismiss='modal'><div class="d-flex justify-content-between align-items-center gap-8 text-large item-check"
                         data-bs-target="#amountModal" data-bs-toggle="modal"
                            onclick="
                                set_storage('crypto', 'currency', '${coin}');
                                set_amount_modal('${coin}', window.wallets['${coin}'])
                                    "
                        data-currency="${coin}">${coin.toUpperCase()} <span class="text-muted font-monospace">${fmtNum(balance)}</span> </div></li>`
                    )
                }
            })
        }

        function w_populate_crypto_for_uid(){
            $('.cryptos-list').html('')
            $.each(window.wallets, function(coin, balance){
                if($.inArray(coin, main_wallets) !== -1 && coin !== 'ngn') {
                    $('.cryptos-list').append(
                        `<li data-bs-dismiss='modal'><div
                            class="d-flex justify-content-between align-items-center gap-8 text-large item-check"
                            data-bs-target="#amountModal" data-bs-toggle="modal"
                            onclick="
                                set_storage('uid', 'currency', '${coin}');
                                set_amount_modal('${coin}', window.wallets['${coin}'])
                                    "
                            data-currency="${coin}">${coin.toUpperCase()} <span class="text-muted font-monospace">${fmtNum(balance)}</span> </div></li>`
                    )
                }
            })
        }

        function w_populate_banks() {
            $('.banks-list').html('')
            $.each(window.user_banks, function (index, details) {
                $('.banks-list').append(
                    `<li data-bs-dismiss='modal'><div class="d-flex justify-content-between align-items-center gap-8 text-large item-check bank-list-item"
                         data-bs-target="#amountModal" data-bs-toggle="modal"
                         data-bank_obj='${JSON.stringify(details)}'
                            onclick="
                                    "
                        data-bank_id="${details.id}">${details.number} (${details.bank}) <i class="icon icon-check-circle" style="display: block"></i> </div></li>`
                )
            })
        }

        function set_amount_modal(curr, bal){
            let action = window.myForm['action']
            let myForm = window.myForm
            $('.w-bal').text(fmtNum(bal));
            $('.w-curr').text(curr.toUpperCase());
            $('.w-bal-after').text(`${fmtNum(bal)} ${curr.toUpperCase()}`);
            $('#w-amount').val(0)
            $('.w-title').text(`${action.toUpperCase()} Withdrawal`)
            $('.w-img').attr('src', `${token_base_url}/${curr}.png`)
            if(curr === 'ngn') {
                w_populate_conf_box()
            }else{
                $('.w-notbank-wallet').css('display', 'block')
                if(action === 'uid'){
                    $('#w-wallet').attr('placeholder', `Enter ${myForm.platform.toUpperCase()} UID`)
                }else{
                    $('#w-wallet').attr('placeholder', `Enter ${myForm.currency.toUpperCase()} (${window.markets[curr]['network']}) Wallet`)
                }
            }
        }

        $('body').on('click', '.bank-list-item', function(){
            set_storage('bank', 'currency', 'ngn');
            window.myForm['bank_obj'] = $(this).attr('data-bank_obj');
            window.myForm['bank_id'] = JSON.parse($(this).attr('data-bank_obj'))['id']
            set_amount_modal('ngn', window.wallets['ngn']);
        })

        function w_populate_conf_box(){
            $('.w-bank-conf').css('display', 'block')
            const bank = JSON.parse(window.myForm.bank_obj)
            $('.w-bank-name').text(bank.name)
            $('.w-bank-number').text(bank.number)
            $('.w-bank-bank').text(bank.bank)
        }

        function w_tag_money(amount, $paste_elem){
            const curr = window.myForm['currency']
            let diff = (window.wallets[curr] - Number(amount)) >= 0 ? window.wallets[curr] - Number(amount) : 0
                if(diff === 0){
                    $('#w-amount').val(window.wallets[curr])
                }
                $paste_elem.text(fmtNum(diff))
        }


        $('#w-amount').keyup(function(){
            if($(this).val() === ""){
                w_tag_money(0, $('.w-bal-after'))
            }else{
                let value = $(this).val()
                if(/^0+/.test(value)){
                    $(this).val(value.replace(/^0+/, ''))
                }
                w_tag_money(value, $('.w-bal-after'))
            }
        })



        function w_final_checks(amount, wallet){
            window.myForm['amount'] = amount
            window.myForm['wallet'] = wallet
            const myForm = window.myForm
            const action = myForm['action']
            const curr = myForm['currency']
            if(window.wallets[curr] - Number(amount) >= 0 && amount > 0){
                if(action !== 'bank' && wallet !== '' || action === 'bank'){
                    if(amount >= window.markets[curr]['min']) {
                        launch_otp('w-confirm-otp')
                        $('#amountModal').modal('hide')
                        $('.otp-title').text('Confirm Withdrawal')
                    }else{
                        notify('warning', `You cannot withdraw below ${window.markets[curr]['min']} ${curr.toUpperCase()}`)
                    }
                }else{
                    notify('warning', 'Please refresh the page and try again')
                }
            }else{
                notify('warning', 'Please check your inputs')
            }
        }

        function withdrawal_complete() {
            const myForm = window.myForm
            showPreloader()
            $.ajax({
                url: withdrawal_base_url,
                type: 'POST',
                dataType: 'json',
                data: myForm,
                success: function (data) {
                    hidePreloader()
                    if (data.status === "success") {
                        $('#amountModal').modal('hide')
                        w_notify(data.amount, data.message, data.medium, '{% url "users:wallet" %}')
                    } else {
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

        $('.w-confirm-otp').click(function () {
            confirm_otp(function () {
                $('#amountModal').modal('show');
                withdrawal_complete()
            })
        })


        function w_notify(amount, message, medium, redirect=null){
            $('.w-notify-amount').text(amount);
            $('.w-notify-message').text(message);
            $('.w-notify-medium').text(medium);
            if(redirect){
                $('.w-notify-done').attr('href', redirect).attr('data-bs-dismiss', '');
            }
            $('#wNotifyModal').modal('show')
        }