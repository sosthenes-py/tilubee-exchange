
        function create_crypto(amount){
            if(amount !== ''){
                $('#cryptoAmountModal').modal('hide')
                const currency = window.myForm['currency']
                let qty;
                qty = (1 / window.markets[currency]['price']) * parseFloat(amount);
                window.myForm['qty'] = qty
                showPreloader()
                $.ajax({
                    url: deposit_base_url,
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        'action': 'retrieve_crypto_wallet',
                        'currency': currency
                    },
                    success: function (data) {
                        hidePreloader()
                        if (data.status === "success") {
                            set_deposit_modal_crypto(data)
                        }else{
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
            }else{
                notify('warning', 'Amount is required to proceed')
            }
        }

        function create_ngn(amount){
            if(amount !== '' && amount > 0){
                $('#bankAmountModal').modal('hide')
                window.myForm['qty'] = Number(amount)
                showPreloader()
                $.ajax({
                    url: deposit_base_url,
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        'action': 'retrieve_bank_account'
                    },
                    success: function (data) {
                        hidePreloader()
                        if (data.status === "success") {
                            set_deposit_modal_bank(data)
                        }else{
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
            }else{
                notify('warning', 'Amount is required to proceed')
            }
        }

        function create_uid(amount){
            if(amount !== '' && amount > 0){
                $('#uidAmountModal').modal('hide')
                const curr = window.myForm['currency']
                let qty;
                qty = (1 / window.markets[curr]['price']) * parseFloat(amount);
                window.myForm['qty'] = qty
                showPreloader()
                $.ajax({
                    url: deposit_base_url,
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        'action': 'retrieve_uid',
                        'platform': window.myForm['platform']
                    },
                    success: function (data) {
                        hidePreloader()
                        if (data.status === "success") {
                            set_deposit_modal_uid(data)
                        }else{
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
            }else{
                notify('warning', 'Amount is required to proceed')
            }
        }


        function set_storage(action, key, value){
            window.myForm['action'] = action
            window.myForm[key] = value
        }

        function reset_storage(){
            window.myForm = {}
        }



        function populate_cryptos(){
            $('.cryptos-list').html('')
            $.each(window.wallets, function(coin, balance){
                if($.inArray(coin, main_wallets) !== -1 && coin !== 'ngn') {
                    $('.cryptos-list').append(
                        `<li data-bs-dismiss='modal'><div class="d-flex justify-content-between align-items-center gap-8 text-large item-check"
                            onclick="
                                set_storage('crypto', 'currency', '${coin}');
                                $('.crypto-bal').text(fmtNum(window.wallets['${coin}']));
                                $('.crypto-curr').text('${coin.toUpperCase()}');
                                $('.crypto-bal-after').text(fmtNum(window.wallets['${coin}']));
                                $('#crypto-amount').val(0)
                                create_crypto(0)
                                    "
                        data-currency="${coin}">${coin.toUpperCase()} <span class="text-muted font-monospace">${fmtNum(balance)}</span> </div></li>`
                    )
                }
            })
        }

        function populate_crypto_for_uid(){
            $('.cryptos-list').html('')
            $.each(window.wallets, function(coin, balance){
                if($.inArray(coin, main_wallets) !== -1 && coin !== 'ngn') {
                    $('.cryptos-list').append(
                        `<li data-bs-dismiss='modal'><div
                            class="d-flex justify-content-between align-items-center gap-8 text-large item-check"
                            data-bs-target="#uidAmountModal" data-bs-toggle="modal"
                            onclick="
                                set_storage('uid', 'currency', '${coin}');
                                $('.uid-bal').text(fmtNum(window.wallets['${coin}']));
                                $('.uid-curr').text('${coin.toUpperCase()}');
                                $('.uid-bal-after').text(fmtNum(window.wallets['${coin}']));
                                $('#uid-amount').val(0)
                                    "
                            data-currency="${coin}">${coin.toUpperCase()} <span class="text-muted font-monospace">${fmtNum(balance)}</span> </div></li>`
                    )
                }
            })
        }

        function set_for_bank(){
            set_storage('bank', 'currency', 'ngn');
            $('.bank-bal').text(fmtNum(window.wallets['ngn']));
            $('.bank-curr').text('NGN');
            $('.bank-bal-after').text(fmtNum(window.wallets['ngn']));
            $('#bank-amount').val(0)
        }



        function tag_money(amount, $paste_elem){
            const uid_curr = window.myForm['currency']
            const to_curr = (1/window.markets[uid_curr]['price']) * parseFloat(amount)
            $paste_elem.text(fmtNum(to_curr + window.wallets[uid_curr]))
        }
        function tag_direct_money(amount, $paste_elem){
            const uid_curr = window.myForm['currency']
            $paste_elem.text(fmtNum(Number(amount) + window.wallets[uid_curr]))
        }

        $('#uid-amount').keyup(function(){
            if($(this).val() === ""){
                tag_money(0, $('.uid-bal-after'))
            }else{
                tag_money($(this).val(), $('.uid-bal-after'))
            }
        })
        $('#bank-amount').keyup(function(){
            if($(this).val() === ""){
                tag_direct_money(0, $('.bank-bal-after'))
            }else{
                tag_direct_money($(this).val(), $('.bank-bal-after'))
            }
        })
        $('#crypto-amount').keyup(function(){
            if($(this).val() === ""){
                tag_money(0, $('.crypto-bal-after'))
            }else{
                tag_money($(this).val(), $('.crypto-bal-after'))
            }
        })

        $('.uid-tag').click(function(){
            tag_money($(this).data('value'), $('.uid-bal-after'))
        })
        $('.bank-tag').click(function(){
            tag_direct_money($(this).data('value'), $('.bank-bal-after'))
        })
        $('.crypto-tag').click(function(){
            tag_money($(this).data('value'), $('.crypto-bal-after'))
        })



        function set_deposit_modal_bank(data){
            // storage::: currency, qty, ref
            $('#actionModal').modal('show')
            $('.action-title').text('Buy with NGN')
            $('.action-body').html(
                `
                <p class="text-center text-small mt-4 action-type">Bank Transfer</p>
                        <h1 class="mt-8 text-center"></h1>
                        <p class="text-center text-small mt-1 text-capitalize">Complete action below to fund your account</p>

                        <ul class="mt-40 accent-box-v4 bg-menuDark action-body">
                            <li class="d-flex align-items-center justify-content-between pb-8 line-bt">
                                <span class="text-small">Account Number</span>
                                <span class="text-large text-white"><i class="icon icon-copy text-muted copy" data-item="${data.number}"></i> ${data.number}</span>
                            </li>
                            <li class="d-flex align-items-center justify-content-between pt-8 pb-8 line-bt">
                                 <span class="text-small">Account Bank </span>
                                 <span class="text-large text-white text-end">${data.bank}</span>
                            </li>
                            <li class="d-flex align-items-center justify-content-between pt-8 pb-8 line-bt">
                                <span class="text-small">Account Name</span>
                                 <span class="text-large text-white text-uppercase"><i class="icon icon-copy text-muted copy" data-item="${data.name}"></i> ${data.name}</span>
                            </li>
                            <li class="d-flex align-items-center justify-content-between pt-8 pb-8 line-bt">
                                <span class="text-small">Amount</span>
                                 <span class="text-large text-white text-uppercase"><i class="icon icon-copy text-muted copy" data-item="${window.myForm['qty']}"></i> &#8358;${fmtNum(window.myForm['qty'])}</span>
                            </li>
                            <li class="d-flex align-items-center justify-content-between pt-8">
                                <span class="text-small">Transfer Narration</span>
                                <span class="text-large text-white"><i class="icon icon-copy text-muted copy" data-item="${data.narration}"></i> ${data.narration}</span>
                            </li>
                        </ul>

                        <ul class='p-1 info-list mt-18'>
                            <li>Ensure to enter the code above in your transfer narration to enable the system confirm your transaction automatically.</li>
                            <li>Ensure to send from a bank account that bears your name as on your profile</li>
                            <li>Ensure to click the button below when transaction is completed</li>
                        </ul>
              
                `
            )
            window.myForm['ref'] = data.narration
        }

        function set_deposit_modal_uid(data){
            // storage::: currency, qty, platform, uid
            $('#actionModal').modal('show')
            $('.action-title').html(`Deposit using UID`)
            $('.action-body').html(
                `
                <p class="text-center text-small mt-4 text-capitalize">${data.platform}</p>
                        <h1 class="mt-8 text-center"></h1>
                        <p class="text-center text-small mt-1 text-capitalize">Complete action below to fund your account</p>

                        <ul class="mt-40 accent-box-v4 bg-menuDark action-body">
                            <li class="d-flex align-items-center justify-content-between pb-8 line-bt">
                                <span class="text-small">Account UID</span>
                                <span class="text-large text-white"><i class="icon icon-copy text-muted copy" data-item="${data.uid}"></i> ${data.uid}</span>
                            </li>
                            <li class="d-flex align-items-center justify-content-between pt-8">
                                <span class="text-small">Quantity</span>
                                <span class="text-large text-white"><i class="icon icon-copy text-muted copy" data-item="${window.myForm['qty']}"></i> ${fmtNum(window.myForm['qty'])} ${window.myForm['currency'].toUpperCase()}</span>
                            </li>

                        </ul>
               
                <ul class='p-1 info-list mt-18'>
                            <li>Ensure to send the exact amount entered previously for quicker confirmation.</li>
                            <li>Ensure to click the button below when transaction is completed</li>
                        </ul>
                `
            )
            window.myForm['uid'] =  data.uid
        }

        function set_deposit_modal_crypto(data){
            // storage::: currency, qty, wallet
            $('#actionModal').modal('show')
            $('.action-title').text('Deposit Crypto')
            $('.action-body').html(
                `
                <p class="text-center text-small mt-4">Crypto Direct Deposit</p>
                        <p class="text-center text-small mt-1 text-capitalize"> Please complete action below to fund your account</p>

                        <ul class="mt-40 accent-box-v4 bg-menuDark action-body">
                            <li class="d-flex align-items-center justify-content-between pb-8 line-bt">
                                <span class="text-small">Crypto</span>
                                <span class="text-large text-white">${data.currency_name} (${data.currency.toUpperCase()})</span>
                            </li>
                            <li class="d-flex align-items-center justify-content-between pt-8 pb-8 line-bt">
                                 <span class="text-small">Chain Type </span>
                                 <span class="text-large text-white text-end">${data.network}</span>
                            </li>
                            <li class="d-flex align-items-center justify-content-between pt-8 pb-8 line-bt">
                                <span class="text-small">Wallet Address</span>
                                 <span class="text-large text-white long-line"><i class="icon icon-copy text-muted copy" data-item="${data.address}"></i> ${trim(data.address)}</span>
                            </li>
                            <li class="d-flex align-items-center justify-content-between pt-8">
                                <span class="text-small">Quantity</span>
                                <span class="text-large text-white"><i class="icon icon-copy text-muted copy" data-item="${window.myForm['qty']}"></i> ${fmtNum(window.myForm['qty'])} ${window.myForm['currency'].toUpperCase()}</span>
                            </li>
                        </ul>
                `
            )
            window.myForm['wallet'] =  data.address
        }

        function deposit_complete(){
            const myForm = window.myForm
            if(myForm.action !== 'crypto'){
                if(myForm.qty > 0 && myForm.currency !== ''){
                    showPreloader()
                    $.ajax({
                        url: deposit_base_url,
                        type: 'POST',
                        dataType: 'json',
                        data: myForm,
                        success: function (data) {
                            hidePreloader()
                            if (data.status === "success") {
                                notifyAmount(`${fmtNum(myForm.qty)} ${myForm.currency.toUpperCase()}`, data.message, null, '{% url "users:wallet" %}')
                            }else{
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
                }else{
                    notify('warning', 'Quantity or currency not found')
                }
            }else{
                $('#actionModal').modal('hide')
            }
        }