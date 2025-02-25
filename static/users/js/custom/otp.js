

   function startCountdown(seconds){
       countdown(seconds, 'countdown', function (){
           $('.resend').html(`Resend in&nbsp;<span id="countdown" ></span>`).css('text-decoration', 'none');
       } ,function (){
           $('.resend').attr('id', 'resend').text('Resend').css('text-decoration', 'underline');
       })
   }

   function confirm_otp(callback){
       event.preventDefault();
       let formData = $('#otp-form').serialize();
       showPreloader()
       $.ajax({
         url : verify_email_url,
         type: 'POST',
         dataType: 'json',
         data: formData,
         success: function(data){
             if(data.status === "success"){
                 $('#otpModal').modal('hide')
                 callback()
             }else{
                 hidePreloader()
                 notify(data.status, data.message)
             }
         },
           error: function(xhr, ajaxOptions, thrownError){
             hidePreloader()
             notify('error', xhr.status + ': ' + xhr.statusText)
           },
           beforeSend: function (xhr, settings){
               xhr.setRequestHeader("X-CSRFToken", csrf_token)
           }
       })
   }

   $('body').on('click', '#resend', function(){
       showPreloader()
       $.ajax({
         url : verify_email_url,
         type: 'POST',
         dataType: 'json',
         data: {'operation': 'resend'},
         success: function(data){
             hidePreloader()
             notify_kwarg({status: data.status, message: data.message, timeout: 2500})
             $('.resend').removeAttr('id')
             startCountdown(100)
         },
           error: function(xhr, ajaxOptions, thrownError){
             hidePreloader()
             notify('error', xhr.status + ': ' + xhr.statusText)
           },
           beforeSend: function (xhr, settings){
               xhr.setRequestHeader("X-CSRFToken", csrf_token)
           }
       })
   })

   

   function launch_otp(add_class){
       $('.otp-block-inputs input').each(function(){
           $(this).val('')
       })
       $('#otpModal').modal('show')
       $('#confirm-otp').addClass(add_class)
   }

   
