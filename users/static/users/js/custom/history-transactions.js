function populate_recent_history(history) {
            $('.history-list').html('')
            $.each(history, function (index, d) {
                if(index <= 50){
                    let status_class = (d.type === 'deposit') ? 'success' : 'danger'
                    if(d.status === 'pending'){
                        status_class = 'warning'
                    }else if(d.status === 'failed'){
                        status_class = 'danger'
                    }
                    const status_sign = (d.type === 'deposit') ? '+' : '-'
                    const mt = (index === 0) ? '' : 'mt-8'
                    $('.history-list').append(
                        `<li class="${mt}">
                                    <a href="#0" class="coin-item style-1 gap-12 bg-surface history-row"
                                    data-title="${d.type} Details"
                                    data-qty="${d.qty}"
                                    data-status="${d.status}"
                                    data-fee="${d.fee}"
                                    data-currency="${d.currency}"
                                    data-time="${d.created_at}"
                                    data-address="${d.address}"
                                    data-hash="${d.hash}"
                                    data-ref="${d.reference}"
                                    data-medium="${d.medium}"
                                    >
                                        <img src="${token_base_url}/${d.currency}.png" alt="img" class="img">
                                        <div class="content">
                                            <div class="title">
                                                <p class="mb-4 text-large">${d.currency_name}</p>
                                                <span class="text-secondary">${d.created_at}</span>
                                            </div>
                                            <div class="box-price">
                                                <p class="text-small mb-4"><span class="text-${status_class}">${status_sign}</span> ${fmtNum(d.qty)} ${d.currency.toUpperCase()}</p>
                                            </div>
                                        </div>
                                    </a>
                                </li>`
                    )
                }
            })
        }
