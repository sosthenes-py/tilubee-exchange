function populate_recent_convs(history, bg) {
    bg = bg || 'bg-surface'
    $('.conversions-list').html('')
    $.each(history, function (index, details) {
        if (index <= 20) {
            $('.conversions-list').append(
                ` <li>
                       <a href="#0" class="coin-item style-1 gap-12 ${bg}">
                           <img src="${token_base_url}/${details.currency_from}.png" alt="img" class="img conv-img">
                           <i class="icon-select-right"></i>
                           <img src="${token_base_url}/${details.currency_to}.png" alt="img" class="img conv-img">
                           <div class="content">
                               <div class="title">
                                   <p class="mb-4 text-danger">${fmtNum(details.qty_from)} ${details.currency_from.toUpperCase()}</p>
                                   <span class="text-success">${fmtNum(details.qty_to)} ${details.currency_to.toUpperCase()}</span>
                               </div>
                               <div class="d-flex align-items-center gap-12">
                                   <span class="text-secondary">${details.created_at}</span>
                                   <span class="coin-btn increase">Done</span>
                               </div>
                           </div>
                       </a>
                   </li>`
            )
        }
    })
}
