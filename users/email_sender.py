from django.core.mail import EmailMessage

SITE_DOMAIN = "iqtradepro.ca"
SITE_NAME = "PROJECT_NAME"


class EmailSender:
    """
    All reasons expect email kwarg
    ...
    Registration requires the following kwargs:
    name (single name of user)
    code (code generated during registration)
    email (email address of user)
    """

    def __init__(self, reason, **kwargs):
        self.reason = reason
        self.kwargs = kwargs
        data = {
            "registration":
                {
                    "subject": f"Welcome to {SITE_NAME}!",
                },
            "withdrawal_bank":
                {
                    "subject": f"Withdrawal is being processed!",
                },
            "withdrawal_crypto":
                {
                    "subject": f"Withdrawal is being processed!",
                },
            "investment":
                {
                    "subject": f"Investment initiated successfully!",
                },
            "docs_approve":
                {
                    "subject": "KYC verification successful"
                },
            "docs_reject":
                {
                    "subject": "We could not verify your identity"
                },
            "approve_deposit":
                {
                    "subject": "Deposit Confirmed"
                },
            "reject_deposit":
                {
                    "subject": "Deposit Failed"
                },
            "set_password":
                {
                    "subject": "Set A Password"
                },
            "otp":
                {
                    "subject": "Your OTP is Here"
                },
            "reset_password":
                {
                    "subject": "Confirm Password Reset"
                }
        }
        self.use = data[self.reason]

        self.email = EmailMessage(
            subject=self.use["subject"],
            from_email=f'{SITE_NAME} <support@{SITE_DOMAIN}>',
            to=[self.kwargs['email']]
        )
        self.email.content_subtype = "html"

    def send_email(self):
        pass
        # self.email.send(fail_silently=True)

    def format_msg(self):
        if self.reason == "registration":
            return f"""

   <div style="padding:0">
   <table align="center" style="background-color:#e9ebee;width:100%;max-width:100%;min-width:100%" border="0" cellpadding="0" cellspacing="0" width="100%">
      <tbody>
         <tr align="center">
            <td style="width:100%;height:20px"></td>
         </tr>
         <tr align="center">
            <td align="center">
               <table border="0" cellpadding="0" cellspacing="0" width="100%">
                  <tbody>
                     <tr>
                        <td>

                           <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                              <tbody>
                                 <tr align="center">
                                    <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#01344B;padding:0;background-color:#01344B">
                                       <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                          <tbody>
                                             <tr align="center">
                                                <td style="text-align:center;border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%"><img width="70" height="" src="https://iqtradepro.ca/static/img/logo-icon.png" style="border:0;max-width:100%" alt="Header" title="Image" class="CToWUd" data-bit="iit" jslog="138226; u014N:xr6bB; 53:WzAsMl0."></td>
                                             </tr>
                                             <tr align="center">
                                                <td style="width:100%;height:0"></td>
                                             </tr>
                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                                 <tr align="center">
                                    <td style="width:100%;height:21px"></td>
                                 </tr>
                              </tbody>
                           </table>
                           <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                              <tbody>
                                 <tr align="center">
                                    <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#fbfbfc;background-color:#ffffff">

                                       <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                          <tbody>
                                             <tr align="center">
                                                <td style="text-align:left;border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;font-family:SF Pro Text;font-size:15px;line-height:20px;letter-spacing:-0.24px;color:#050505">
                                                   Hi {self.kwargs['name']}, 


                                                   <p>
                                                      Almost done!
                                       <br><br>
                                       To complete your {SITE_NAME} signup, please use the code below to verify your email address ({self.kwargs['email']}) on the website
                                                   </p>




                                                   <div>
                                                      <div style="padding-top:16px;padding-bottom:16px;text-align:left">

                                                         <div style="padding-bottom:15px;text-align:center">

                                                            <tr align="center">
                                                               <td style="width:100%;height:5px"></td>
                                                            </tr>


 <!-- BUTTON                                                            -->
<table border="0" width="100%" cellspacing="0" cellpadding="0" style="border-collapse:collapse">
   <tbody>
      <tr>
         <td height="2" style="line-height:2px">&nbsp;</td>
      </tr>
      <tr>
         <td align="middle">
            <div style="font-family: monospace; font-size: 1.4em">{self.kwargs['code']}</div>
            </td>
      </tr>
      <tr>
         <td height="8" style="line-height:8px">&nbsp;</td>
      </tr>
      <tr>
         <td height="0" style="line-height:0px">&nbsp;</td>
      </tr>
   </tbody>
</table>





                                                         </div>
                                                      </div>

                                                   </div>



                                                </td>
                                             </tr>
                                             <tr align="center">
                                                <td style="width:100%;height:30px"></td>
                                             </tr>
                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                                 <tr align="center">
                                    <td style="width:100%;height:5px"></td>
                                 </tr>
                              </tbody>
                           </table>
                           <table style="width:100%" align="center">
                              <tbody>
                                 <tr align="center">
                                    <td>
                                       <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                                          <tbody>
                                             <tr align="center">
                                                <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#fbfbfc;padding:20px 0px 0px 0px;background-color:#e9ebee">
                                                   <div>
                                                      <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                         <tbody>
                                                            <tr align="center">
                                                               <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;color:#8f949b;font-size:12px;padding:0 20px">

                                                                  Trading Forex and CFDs involves significant risk and can result in the loss of your invested capital. You should not invest more than you can afford to lose and should ensure that you fully understand the risks involved. <br>
                                                                  *Past Performance does not guarantee future returns.

                                                                  </td>
                                                            </tr>
                                                            <tr align="center">
                                                               <td style="width:100%;height:15px"></td>
                                                            </tr>
                                                         </tbody>
                                                      </table>
                                                      <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                         <tbody>
                                                            <tr align="center">
                                                               <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;background-color:#979797;width:100%;height:1px"></td>
                                                            </tr>
                                                            <tr align="center">
                                                               <td style="width:100%;height:15px"></td>
                                                            </tr>
                                                         </tbody>
                                                      </table>
                                                   </div>
                                                   <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                      <tbody>
                                                         <tr align="center">
                                                            <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;color:#8f949b;font-size:12px;padding:0 64px">QtradeInvest Direct Investing<br>
                                                               700 - 1111 West Georgia Street<br>
                                                               Vancouver, BC V6E 4T6</td>
                                                         </tr>
                                                         <tr align="center">
                                                            <td style="width:100%;height:0"></td>
                                                         </tr>
                                                      </tbody>
                                                   </table>
                                                </td>
                                             </tr>

                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                              </tbody>
                           </table>
                        </td>
                     </tr>
                  </tbody>
               </table>
            </td>
         </tr>
         <tr align="center">
            <td style="width:100%;height:30px"></td>
         </tr>

      </tbody>
   </table>
</div>
            """
        elif self.reason == "withdrawal_bank":
            return f"""

            <div style="padding:0">
   <table align="center" style="background-color:#e9ebee;width:100%;max-width:100%;min-width:100%" border="0" cellpadding="0" cellspacing="0" width="100%">
      <tbody>
         <tr align="center">
            <td style="width:100%;height:20px"></td>
         </tr>
         <tr align="center">
            <td align="center">
               <table border="0" cellpadding="0" cellspacing="0" width="100%">
                  <tbody>
                     <tr>
                        <td>

                           <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                              <tbody>
                                 <tr align="center">
                                    <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#01344B;padding:0;background-color:#01344B">
                                       <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                          <tbody>
                                             <tr align="center">
                                                <td style="text-align:center;border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%"><img width="70" height="" src="https://iqtradepro.ca/static/img/logo-icon.png" style="border:0;max-width:100%" alt="Header" title="Image" class="CToWUd" data-bit="iit" jslog="138226; u014N:xr6bB; 53:WzAsMl0."></td>
                                             </tr>
                                             <tr align="center">
                                                <td style="width:100%;height:0"></td>
                                             </tr>
                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                                 <tr align="center">
                                    <td style="width:100%;height:21px"></td>
                                 </tr>
                              </tbody>
                           </table>
                           <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                              <tbody>
                                 <tr align="center">
                                    <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#fbfbfc;background-color:#ffffff">

                                       <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                          <tbody>
                                             <tr align="center">
                                                <td style="text-align:left;border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;font-family:SF Pro Text;font-size:15px;line-height:20px;letter-spacing:-0.24px;color:#050505">
                                                   Hi, 


                                                   <p>
                                                      This is to inform you that your withdrawal of {self.kwargs['amount']} USD to {self.kwargs['bank_name']} ({self.kwargs['acct_no']}) has been received and is being processed.
                                                   </p>
                                                   <p>You will hear from us again as soon as this process has been completed. Thank you.</p>



                                                   <div>
                                                      <div style="padding-top:16px;padding-bottom:16px;text-align:left">

                                                         <div style="padding-bottom:15px;text-align:center">

                                                            <tr align="center">
                                                               <td style="width:100%;height:5px"></td>
                                                            </tr>


                                                         </div>
                                                      </div>

                                                   </div>



                                                </td>
                                             </tr>
                                             <tr align="center">
                                                <td style="width:100%;height:30px"></td>
                                             </tr>
                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                                 <tr align="center">
                                    <td style="width:100%;height:5px"></td>
                                 </tr>
                              </tbody>
                           </table>
                           <table style="width:100%" align="center">
                              <tbody>
                                 <tr align="center">
                                    <td>
                                       <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                                          <tbody>
                                             <tr align="center">
                                                <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#fbfbfc;padding:20px 0px 0px 0px;background-color:#e9ebee">
                                                   <div>
                                                      <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                         <tbody>
                                                            <tr align="center">
                                                               <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;color:#8f949b;font-size:12px;padding:0 20px">

                                                                  Trading Forex and CFDs involves significant risk and can result in the loss of your invested capital. You should not invest more than you can afford to lose and should ensure that you fully understand the risks involved. <br>
                                                                  *Past Performance does not guarantee future returns.

                                                                  </td>
                                                            </tr>
                                                            <tr align="center">
                                                               <td style="width:100%;height:15px"></td>
                                                            </tr>
                                                         </tbody>
                                                      </table>
                                                      <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                         <tbody>
                                                            <tr align="center">
                                                               <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;background-color:#979797;width:100%;height:1px"></td>
                                                            </tr>
                                                            <tr align="center">
                                                               <td style="width:100%;height:15px"></td>
                                                            </tr>
                                                         </tbody>
                                                      </table>
                                                   </div>
                                                   <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                      <tbody>
                                                         <tr align="center">
                                                            <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;color:#8f949b;font-size:12px;padding:0 64px">QtradeInvest Direct Investing<br>
                                                               700 - 1111 West Georgia Street<br>
                                                               Vancouver, BC V6E 4T6</td>
                                                         </tr>
                                                         <tr align="center">
                                                            <td style="width:100%;height:0"></td>
                                                         </tr>
                                                      </tbody>
                                                   </table>
                                                </td>
                                             </tr>

                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                              </tbody>
                           </table>
                        </td>
                     </tr>
                  </tbody>
               </table>
            </td>
         </tr>
         <tr align="center">
            <td style="width:100%;height:30px"></td>
         </tr>

      </tbody>
   </table>
</div>

            """
        elif self.reason == "withdrawal_crypto":
            return f"""

            <div style="padding:0">
   <table align="center" style="background-color:#e9ebee;width:100%;max-width:100%;min-width:100%" border="0" cellpadding="0" cellspacing="0" width="100%">
      <tbody>
         <tr align="center">
            <td style="width:100%;height:20px"></td>
         </tr>
         <tr align="center">
            <td align="center">
               <table border="0" cellpadding="0" cellspacing="0" width="100%">
                  <tbody>
                     <tr>
                        <td>

                           <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                              <tbody>
                                 <tr align="center">
                                    <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#01344B;padding:0;background-color:#01344B">
                                       <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                          <tbody>
                                             <tr align="center">
                                                <td style="text-align:center;border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%"><img width="70" height="" src="https://iqtradepro.ca/static/img/logo-icon.png" style="border:0;max-width:100%" alt="Header" title="Image" class="CToWUd" data-bit="iit" jslog="138226; u014N:xr6bB; 53:WzAsMl0."></td>
                                             </tr>
                                             <tr align="center">
                                                <td style="width:100%;height:0"></td>
                                             </tr>
                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                                 <tr align="center">
                                    <td style="width:100%;height:21px"></td>
                                 </tr>
                              </tbody>
                           </table>
                           <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                              <tbody>
                                 <tr align="center">
                                    <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#fbfbfc;background-color:#ffffff">

                                       <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                          <tbody>
                                             <tr align="center">
                                                <td style="text-align:left;border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;font-family:SF Pro Text;font-size:15px;line-height:20px;letter-spacing:-0.24px;color:#050505">
                                                   Hi, 


                                                   <p>
                                                      This is to inform you that your withdrawal of {self.kwargs['amount']} USD ({self.kwargs['qty']} {self.kwargs['curr']}) has been received and is being processed.
                                                   </p>

                                                   <p>We will let you know as soon as this process has been completed.</p>


                                                   <div>
                                                      <div style="padding-top:16px;padding-bottom:16px;text-align:left">

                                                         <div style="padding-bottom:15px;text-align:center">

                                                            <tr align="center">
                                                               <td style="width:100%;height:5px"></td>
                                                            </tr>






                                                         </div>
                                                      </div>

                                                   </div>



                                                </td>
                                             </tr>
                                             <tr align="center">
                                                <td style="width:100%;height:30px"></td>
                                             </tr>
                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                                 <tr align="center">
                                    <td style="width:100%;height:5px"></td>
                                 </tr>
                              </tbody>
                           </table>
                           <table style="width:100%" align="center">
                              <tbody>
                                 <tr align="center">
                                    <td>
                                       <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                                          <tbody>
                                             <tr align="center">
                                                <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#fbfbfc;padding:20px 0px 0px 0px;background-color:#e9ebee">
                                                   <div>
                                                      <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                         <tbody>
                                                            <tr align="center">
                                                               <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;color:#8f949b;font-size:12px;padding:0 20px">

                                                                  Trading Forex and CFDs involves significant risk and can result in the loss of your invested capital. You should not invest more than you can afford to lose and should ensure that you fully understand the risks involved. <br>
                                                                  *Past Performance does not guarantee future returns.

                                                                  </td>
                                                            </tr>
                                                            <tr align="center">
                                                               <td style="width:100%;height:15px"></td>
                                                            </tr>
                                                         </tbody>
                                                      </table>
                                                      <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                         <tbody>
                                                            <tr align="center">
                                                               <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;background-color:#979797;width:100%;height:1px"></td>
                                                            </tr>
                                                            <tr align="center">
                                                               <td style="width:100%;height:15px"></td>
                                                            </tr>
                                                         </tbody>
                                                      </table>
                                                   </div>
                                                   <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                      <tbody>
                                                         <tr align="center">
                                                            <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;color:#8f949b;font-size:12px;padding:0 64px">QtradeInvest Direct Investing<br>
                                                               700 - 1111 West Georgia Street<br>
                                                               Vancouver, BC V6E 4T6</td>
                                                         </tr>
                                                         <tr align="center">
                                                            <td style="width:100%;height:0"></td>
                                                         </tr>
                                                      </tbody>
                                                   </table>
                                                </td>
                                             </tr>

                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                              </tbody>
                           </table>
                        </td>
                     </tr>
                  </tbody>
               </table>
            </td>
         </tr>
         <tr align="center">
            <td style="width:100%;height:30px"></td>
         </tr>

      </tbody>
   </table>
</div>

            """
        elif self.reason == "investment":
            return f"""

            <div style="padding:0">
   <table align="center" style="background-color:#e9ebee;width:100%;max-width:100%;min-width:100%" border="0" cellpadding="0" cellspacing="0" width="100%">
      <tbody>
         <tr align="center">
            <td style="width:100%;height:20px"></td>
         </tr>
         <tr align="center">
            <td align="center">
               <table border="0" cellpadding="0" cellspacing="0" width="100%">
                  <tbody>
                     <tr>
                        <td>

                           <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                              <tbody>
                                 <tr align="center">
                                    <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#01344B;padding:0;background-color:#01344B">
                                       <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                          <tbody>
                                             <tr align="center">
                                                <td style="text-align:center;border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%"><img width="70" height="" src="https://iqtradepro.ca/static/img/logo-icon.png" style="border:0;max-width:100%" alt="Header" title="Image" class="CToWUd" data-bit="iit" jslog="138226; u014N:xr6bB; 53:WzAsMl0."></td>
                                             </tr>
                                             <tr align="center">
                                                <td style="width:100%;height:0"></td>
                                             </tr>
                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                                 <tr align="center">
                                    <td style="width:100%;height:21px"></td>
                                 </tr>
                              </tbody>
                           </table>
                           <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                              <tbody>
                                 <tr align="center">
                                    <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#fbfbfc;background-color:#ffffff">

                                       <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                          <tbody>
                                             <tr align="center">
                                                <td style="text-align:left;border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;font-family:SF Pro Text;font-size:15px;line-height:20px;letter-spacing:-0.24px;color:#050505">
                                                   Hi, 


                                                   <p >
                                                      Investment of {self.kwargs['amount']:,} USD to the {self.kwargs['name']} plan has been initiated successfully
                                                   </p>

                                                   <p>You will continue to receive updates regarding this investment with time.</p>

                                                   <div>
                                                      <div style="padding-top:16px;padding-bottom:16px;text-align:left">

                                                         <div style="padding-bottom:15px;text-align:center">

                                                            <tr align="center">
                                                               <td style="width:100%;height:5px"></td>
                                                            </tr>



                                                         </div>
                                                      </div>

                                                   </div>



                                                </td>
                                             </tr>
                                             <tr align="center">
                                                <td style="width:100%;height:30px"></td>
                                             </tr>
                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                                 <tr align="center">
                                    <td style="width:100%;height:5px"></td>
                                 </tr>
                              </tbody>
                           </table>
                           <table style="width:100%" align="center">
                              <tbody>
                                 <tr align="center">
                                    <td>
                                       <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                                          <tbody>
                                             <tr align="center">
                                                <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#fbfbfc;padding:20px 0px 0px 0px;background-color:#e9ebee">
                                                   <div>
                                                      <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                         <tbody>
                                                            <tr align="center">
                                                               <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;color:#8f949b;font-size:12px;padding:0 20px">

                                                                  Trading Forex and CFDs involves significant risk and can result in the loss of your invested capital. You should not invest more than you can afford to lose and should ensure that you fully understand the risks involved. <br>
                                                                  *Past Performance does not guarantee future returns.

                                                                  </td>
                                                            </tr>
                                                            <tr align="center">
                                                               <td style="width:100%;height:15px"></td>
                                                            </tr>
                                                         </tbody>
                                                      </table>
                                                      <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                         <tbody>
                                                            <tr align="center">
                                                               <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;background-color:#979797;width:100%;height:1px"></td>
                                                            </tr>
                                                            <tr align="center">
                                                               <td style="width:100%;height:15px"></td>
                                                            </tr>
                                                         </tbody>
                                                      </table>
                                                   </div>
                                                   <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                      <tbody>
                                                         <tr align="center">
                                                            <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;color:#8f949b;font-size:12px;padding:0 64px">QtradeInvest Direct Investing<br>
                                                               700 - 1111 West Georgia Street<br>
                                                               Vancouver, BC V6E 4T6</td>
                                                         </tr>
                                                         <tr align="center">
                                                            <td style="width:100%;height:0"></td>
                                                         </tr>
                                                      </tbody>
                                                   </table>
                                                </td>
                                             </tr>

                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                              </tbody>
                           </table>
                        </td>
                     </tr>
                  </tbody>
               </table>
            </td>
         </tr>
         <tr align="center">
            <td style="width:100%;height:30px"></td>
         </tr>

      </tbody>
   </table>
</div>

            """
        elif self.reason == "docs_approve":
            return f"""

            <div style="padding:0">
   <table align="center" style="background-color:#e9ebee;width:100%;max-width:100%;min-width:100%" border="0" cellpadding="0" cellspacing="0" width="100%">
      <tbody>
         <tr align="center">
            <td style="width:100%;height:20px"></td>
         </tr>
         <tr align="center">
            <td align="center">
               <table border="0" cellpadding="0" cellspacing="0" width="100%">
                  <tbody>
                     <tr>
                        <td>

                           <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                              <tbody>
                                 <tr align="center">
                                    <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#01344B;padding:0;background-color:#01344B">
                                       <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                          <tbody>
                                             <tr align="center">
                                                <td style="text-align:center;border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%"><img width="70" height="" src="https://iqtradepro.ca/static/img/logo-icon.png" style="border:0;max-width:100%" alt="Header" title="Image" class="CToWUd" data-bit="iit" jslog="138226; u014N:xr6bB; 53:WzAsMl0."></td>
                                             </tr>
                                             <tr align="center">
                                                <td style="width:100%;height:0"></td>
                                             </tr>
                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                                 <tr align="center">
                                    <td style="width:100%;height:21px"></td>
                                 </tr>
                              </tbody>
                           </table>
                           <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                              <tbody>
                                 <tr align="center">
                                    <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#fbfbfc;background-color:#ffffff">

                                       <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                          <tbody>
                                             <tr align="center">
                                                <td style="text-align:left;border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;font-family:SF Pro Text;font-size:15px;line-height:20px;letter-spacing:-0.24px;color:#050505">
                                                   Hi, 


                                                   <p >
                                                      Your ID verification was completed successfully.
                                                   </p>



                                                   <div>
                                                      <div style="padding-top:16px;padding-bottom:16px;text-align:left">

                                                         <div style="padding-bottom:15px;text-align:center">

                                                            <tr align="center">
                                                               <td style="width:100%;height:5px"></td>
                                                            </tr>




                                                         </div>
                                                      </div>

                                                   </div>



                                                </td>
                                             </tr>
                                             <tr align="center">
                                                <td style="width:100%;height:30px"></td>
                                             </tr>
                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                                 <tr align="center">
                                    <td style="width:100%;height:5px"></td>
                                 </tr>
                              </tbody>
                           </table>
                           <table style="width:100%" align="center">
                              <tbody>
                                 <tr align="center">
                                    <td>
                                       <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                                          <tbody>
                                             <tr align="center">
                                                <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#fbfbfc;padding:20px 0px 0px 0px;background-color:#e9ebee">
                                                   <div>
                                                      <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                         <tbody>
                                                            <tr align="center">
                                                               <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;color:#8f949b;font-size:12px;padding:0 20px">

                                                                  Trading Forex and CFDs involves significant risk and can result in the loss of your invested capital. You should not invest more than you can afford to lose and should ensure that you fully understand the risks involved. <br>
                                                                  *Past Performance does not guarantee future returns.

                                                                  </td>
                                                            </tr>
                                                            <tr align="center">
                                                               <td style="width:100%;height:15px"></td>
                                                            </tr>
                                                         </tbody>
                                                      </table>
                                                      <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                         <tbody>
                                                            <tr align="center">
                                                               <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;background-color:#979797;width:100%;height:1px"></td>
                                                            </tr>
                                                            <tr align="center">
                                                               <td style="width:100%;height:15px"></td>
                                                            </tr>
                                                         </tbody>
                                                      </table>
                                                   </div>
                                                   <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                      <tbody>
                                                         <tr align="center">
                                                            <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;color:#8f949b;font-size:12px;padding:0 64px">QtradeInvest Direct Investing<br>
                                                               700 - 1111 West Georgia Street<br>
                                                               Vancouver, BC V6E 4T6</td>
                                                         </tr>
                                                         <tr align="center">
                                                            <td style="width:100%;height:0"></td>
                                                         </tr>
                                                      </tbody>
                                                   </table>
                                                </td>
                                             </tr>

                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                              </tbody>
                           </table>
                        </td>
                     </tr>
                  </tbody>
               </table>
            </td>
         </tr>
         <tr align="center">
            <td style="width:100%;height:30px"></td>
         </tr>

      </tbody>
   </table>
</div>

            """
        elif self.reason == "docs_reject":
            return f"""

            <div style="padding:0">
   <table align="center" style="background-color:#e9ebee;width:100%;max-width:100%;min-width:100%" border="0" cellpadding="0" cellspacing="0" width="100%">
      <tbody>
         <tr align="center">
            <td style="width:100%;height:20px"></td>
         </tr>
         <tr align="center">
            <td align="center">
               <table border="0" cellpadding="0" cellspacing="0" width="100%">
                  <tbody>
                     <tr>
                        <td>

                           <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                              <tbody>
                                 <tr align="center">
                                    <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#01344B;padding:0;background-color:#01344B">
                                       <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                          <tbody>
                                             <tr align="center">
                                                <td style="text-align:center;border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%"><img width="70" height="" src="https://iqtradepro.ca/static/img/logo-icon.png" style="border:0;max-width:100%" alt="Header" title="Image" class="CToWUd" data-bit="iit" jslog="138226; u014N:xr6bB; 53:WzAsMl0."></td>
                                             </tr>
                                             <tr align="center">
                                                <td style="width:100%;height:0"></td>
                                             </tr>
                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                                 <tr align="center">
                                    <td style="width:100%;height:21px"></td>
                                 </tr>
                              </tbody>
                           </table>
                           <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                              <tbody>
                                 <tr align="center">
                                    <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#fbfbfc;background-color:#ffffff">

                                       <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                          <tbody>
                                             <tr align="center">
                                                <td style="text-align:left;border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;font-family:SF Pro Text;font-size:15px;line-height:20px;letter-spacing:-0.24px;color:#050505">
                                                   Hi, 

                                                   <p >
                                                      We regret to let you know that we could not verify your identity. <br>
                                                 The following could be the cause: Non-clear or non-readable document, unaccepted document submitted, unaccepted region of application and more.
                                                   </p>

                                                   <p>If you think this was a mistake from your end, you can go to our website to resubmit another document</p>



                                                   <div>
                                                      <div style="padding-top:16px;padding-bottom:16px;text-align:left">

                                                         <div style="padding-bottom:15px;text-align:center">

                                                            <tr align="center">
                                                               <td style="width:100%;height:5px"></td>
                                                            </tr>




                                                         </div>
                                                      </div>

                                                   </div>



                                                </td>
                                             </tr>
                                             <tr align="center">
                                                <td style="width:100%;height:30px"></td>
                                             </tr>
                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                                 <tr align="center">
                                    <td style="width:100%;height:5px"></td>
                                 </tr>
                              </tbody>
                           </table>
                           <table style="width:100%" align="center">
                              <tbody>
                                 <tr align="center">
                                    <td>
                                       <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                                          <tbody>
                                             <tr align="center">
                                                <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#fbfbfc;padding:20px 0px 0px 0px;background-color:#e9ebee">
                                                   <div>
                                                      <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                         <tbody>
                                                            <tr align="center">
                                                               <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;color:#8f949b;font-size:12px;padding:0 20px">

                                                                  Trading Forex and CFDs involves significant risk and can result in the loss of your invested capital. You should not invest more than you can afford to lose and should ensure that you fully understand the risks involved. <br>
                                                                  *Past Performance does not guarantee future returns.

                                                                  </td>
                                                            </tr>
                                                            <tr align="center">
                                                               <td style="width:100%;height:15px"></td>
                                                            </tr>
                                                         </tbody>
                                                      </table>
                                                      <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                         <tbody>
                                                            <tr align="center">
                                                               <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;background-color:#979797;width:100%;height:1px"></td>
                                                            </tr>
                                                            <tr align="center">
                                                               <td style="width:100%;height:15px"></td>
                                                            </tr>
                                                         </tbody>
                                                      </table>
                                                   </div>
                                                   <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                      <tbody>
                                                         <tr align="center">
                                                            <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;color:#8f949b;font-size:12px;padding:0 64px">QtradeInvest Direct Investing<br>
                                                               700 - 1111 West Georgia Street<br>
                                                               Vancouver, BC V6E 4T6</td>
                                                         </tr>
                                                         <tr align="center">
                                                            <td style="width:100%;height:0"></td>
                                                         </tr>
                                                      </tbody>
                                                   </table>
                                                </td>
                                             </tr>

                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                              </tbody>
                           </table>
                        </td>
                     </tr>
                  </tbody>
               </table>
            </td>
         </tr>
         <tr align="center">
            <td style="width:100%;height:30px"></td>
         </tr>

      </tbody>
   </table>
</div>

            """
        elif self.reason == "approve_deposit":
            return f"""

            <div style="padding:0">
   <table align="center" style="background-color:#e9ebee;width:100%;max-width:100%;min-width:100%" border="0" cellpadding="0" cellspacing="0" width="100%">
      <tbody>
         <tr align="center">
            <td style="width:100%;height:20px"></td>
         </tr>
         <tr align="center">
            <td align="center">
               <table border="0" cellpadding="0" cellspacing="0" width="100%">
                  <tbody>
                     <tr>
                        <td>

                           <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                              <tbody>
                                 <tr align="center">
                                    <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#01344B;padding:0;background-color:#01344B">
                                       <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                          <tbody>
                                             <tr align="center">
                                                <td style="text-align:center;border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%"><img width="70" height="" src="https://iqtradepro.ca/static/img/logo-icon.png" style="border:0;max-width:100%" alt="Header" title="Image" class="CToWUd" data-bit="iit" jslog="138226; u014N:xr6bB; 53:WzAsMl0."></td>
                                             </tr>
                                             <tr align="center">
                                                <td style="width:100%;height:0"></td>
                                             </tr>
                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                                 <tr align="center">
                                    <td style="width:100%;height:21px"></td>
                                 </tr>
                              </tbody>
                           </table>
                           <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                              <tbody>
                                 <tr align="center">
                                    <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#fbfbfc;background-color:#ffffff">

                                       <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                          <tbody>
                                             <tr align="center">
                                                <td style="text-align:left;border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;font-family:SF Pro Text;font-size:15px;line-height:20px;letter-spacing:-0.24px;color:#050505">
                                                   Hi, 

                                                   <p >
                                                      Your deposit of {self.kwargs['qty']} {self.kwargs['method']} (${self.kwargs['amt']}) is now available in your account.<br>
                                                      You may login to check!<br><br>
                                                     Transaction ID is:
                                                      <h4>#TX-{self.kwargs['id']}</h4>
                                                      Thank you.
                                                   </p>



                                                   <div>
                                                      <div style="padding-top:16px;padding-bottom:16px;text-align:left">

                                                         <div style="padding-bottom:15px;text-align:center">

                                                            <tr align="center">
                                                               <td style="width:100%;height:5px"></td>
                                                            </tr>





                                                         </div>
                                                      </div>

                                                   </div>


                                                </td>
                                             </tr>
                                             <tr align="center">
                                                <td style="width:100%;height:30px"></td>
                                             </tr>
                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                                 <tr align="center">
                                    <td style="width:100%;height:5px"></td>
                                 </tr>
                              </tbody>
                           </table>
                           <table style="width:100%" align="center">
                              <tbody>
                                 <tr align="center">
                                    <td>
                                       <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                                          <tbody>
                                             <tr align="center">
                                                <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#fbfbfc;padding:20px 0px 0px 0px;background-color:#e9ebee">
                                                   <div>
                                                      <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                         <tbody>
                                                            <tr align="center">
                                                               <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;color:#8f949b;font-size:12px;padding:0 20px">

                                                                  Trading Forex and CFDs involves significant risk and can result in the loss of your invested capital. You should not invest more than you can afford to lose and should ensure that you fully understand the risks involved. <br>
                                                                  *Past Performance does not guarantee future returns.

                                                                  </td>
                                                            </tr>
                                                            <tr align="center">
                                                               <td style="width:100%;height:15px"></td>
                                                            </tr>
                                                         </tbody>
                                                      </table>
                                                      <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                         <tbody>
                                                            <tr align="center">
                                                               <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;background-color:#979797;width:100%;height:1px"></td>
                                                            </tr>
                                                            <tr align="center">
                                                               <td style="width:100%;height:15px"></td>
                                                            </tr>
                                                         </tbody>
                                                      </table>
                                                   </div>
                                                   <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                      <tbody>
                                                         <tr align="center">
                                                            <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;color:#8f949b;font-size:12px;padding:0 64px">QtradeInvest Direct Investing<br>
                                                               700 - 1111 West Georgia Street<br>
                                                               Vancouver, BC V6E 4T6</td>
                                                         </tr>
                                                         <tr align="center">
                                                            <td style="width:100%;height:0"></td>
                                                         </tr>
                                                      </tbody>
                                                   </table>
                                                </td>
                                             </tr>

                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                              </tbody>
                           </table>
                        </td>
                     </tr>
                  </tbody>
               </table>
            </td>
         </tr>
         <tr align="center">
            <td style="width:100%;height:30px"></td>
         </tr>

      </tbody>
   </table>
</div>

            """
        elif self.reason == "reject_deposit":
            return f"""

                              <div style="padding:0">
   <table align="center" style="background-color:#e9ebee;width:100%;max-width:100%;min-width:100%" border="0" cellpadding="0" cellspacing="0" width="100%">
      <tbody>
         <tr align="center">
            <td style="width:100%;height:20px"></td>
         </tr>
         <tr align="center">
            <td align="center">
               <table border="0" cellpadding="0" cellspacing="0" width="100%">
                  <tbody>
                     <tr>
                        <td>

                           <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                              <tbody>
                                 <tr align="center">
                                    <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#01344B;padding:0;background-color:#01344B">
                                       <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                          <tbody>
                                             <tr align="center">
                                                <td style="text-align:center;border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%"><img width="70" height="" src="https://iqtradepro.ca/static/img/logo-icon.png" style="border:0;max-width:100%" alt="Header" title="Image" class="CToWUd" data-bit="iit" jslog="138226; u014N:xr6bB; 53:WzAsMl0."></td>
                                             </tr>
                                             <tr align="center">
                                                <td style="width:100%;height:0"></td>
                                             </tr>
                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                                 <tr align="center">
                                    <td style="width:100%;height:21px"></td>
                                 </tr>
                              </tbody>
                           </table>
                           <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                              <tbody>
                                 <tr align="center">
                                    <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#fbfbfc;background-color:#ffffff">

                                       <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                          <tbody>
                                             <tr align="center">
                                                <td style="text-align:left;border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;font-family:SF Pro Text;font-size:15px;line-height:20px;letter-spacing:-0.24px;color:#050505">
                                                   Hi, 

                                                   <p >
                                                      We regret to let you know that your deposit of {self.kwargs['qty']} {self.kwargs['method']} could not be approved. <br>Please contact us with the ID below for more details.<br>

                                                Transaction ID is:
                                                 <h4>#TX-{self.kwargs['id']}</h4>
                                                 Thank you.
                                                   </p>

                                                   <div>
                                                      <div style="padding-top:16px;padding-bottom:16px;text-align:left">

                                                         <div style="padding-bottom:15px;text-align:center">

                                                            <tr align="center">
                                                               <td style="width:100%;height:5px"></td>
                                                            </tr>





                                                         </div>
                                                      </div>

                                                   </div>


                                                </td>
                                             </tr>
                                             <tr align="center">
                                                <td style="width:100%;height:30px"></td>
                                             </tr>
                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                                 <tr align="center">
                                    <td style="width:100%;height:5px"></td>
                                 </tr>
                              </tbody>
                           </table>
                           <table style="width:100%" align="center">
                              <tbody>
                                 <tr align="center">
                                    <td>
                                       <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                                          <tbody>
                                             <tr align="center">
                                                <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#fbfbfc;padding:20px 0px 0px 0px;background-color:#e9ebee">
                                                   <div>
                                                      <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                         <tbody>
                                                            <tr align="center">
                                                               <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;color:#8f949b;font-size:12px;padding:0 20px">

                                                                  Trading Forex and CFDs involves significant risk and can result in the loss of your invested capital. You should not invest more than you can afford to lose and should ensure that you fully understand the risks involved. <br>
                                                                  *Past Performance does not guarantee future returns.

                                                                  </td>
                                                            </tr>
                                                            <tr align="center">
                                                               <td style="width:100%;height:15px"></td>
                                                            </tr>
                                                         </tbody>
                                                      </table>
                                                      <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                         <tbody>
                                                            <tr align="center">
                                                               <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;background-color:#979797;width:100%;height:1px"></td>
                                                            </tr>
                                                            <tr align="center">
                                                               <td style="width:100%;height:15px"></td>
                                                            </tr>
                                                         </tbody>
                                                      </table>
                                                   </div>
                                                   <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                      <tbody>
                                                         <tr align="center">
                                                            <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;color:#8f949b;font-size:12px;padding:0 64px">QtradeInvest Direct Investing<br>
                                                               700 - 1111 West Georgia Street<br>
                                                               Vancouver, BC V6E 4T6</td>
                                                         </tr>
                                                         <tr align="center">
                                                            <td style="width:100%;height:0"></td>
                                                         </tr>
                                                      </tbody>
                                                   </table>
                                                </td>
                                             </tr>

                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                              </tbody>
                           </table>
                        </td>
                     </tr>
                  </tbody>
               </table>
            </td>
         </tr>
         <tr align="center">
            <td style="width:100%;height:30px"></td>
         </tr>

      </tbody>
   </table>
</div>


                                    """
        elif self.reason == "set_password":
            return f"""

            <div style="padding:0">
   <table align="center" style="background-color:#e9ebee;width:100%;max-width:100%;min-width:100%" border="0" cellpadding="0" cellspacing="0" width="100%">
      <tbody>
         <tr align="center">
            <td style="width:100%;height:20px"></td>
         </tr>
         <tr align="center">
            <td align="center">
               <table border="0" cellpadding="0" cellspacing="0" width="100%">
                  <tbody>
                     <tr>
                        <td>

                           <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                              <tbody>
                                 <tr align="center">
                                    <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#01344B;padding:0;background-color:#01344B">
                                       <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                          <tbody>
                                             <tr align="center">
                                                <td style="text-align:center;border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%"><img width="70" height="" src="https://iqtradepro.ca/static/img/logo-icon.png" style="border:0;max-width:100%" alt="Header" title="Image" class="CToWUd" data-bit="iit" jslog="138226; u014N:xr6bB; 53:WzAsMl0."></td>
                                             </tr>
                                             <tr align="center">
                                                <td style="width:100%;height:0"></td>
                                             </tr>
                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                                 <tr align="center">
                                    <td style="width:100%;height:21px"></td>
                                 </tr>
                              </tbody>
                           </table>
                           <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                              <tbody>
                                 <tr align="center">
                                    <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#fbfbfc;background-color:#ffffff">

                                       <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                          <tbody>
                                             <tr align="center">
                                                <td style="text-align:left;border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;font-family:SF Pro Text;font-size:15px;line-height:20px;letter-spacing:-0.24px;color:#050505">
                                                   Hi {self.kwargs['name']},

                                                   <p>
                                                      We hope this message finds you well. We're excited to inform you that you've been converted to a contact on QTrade Pro!
                                                             <br><br>
                                                             Here's what you need to do to complete your account setup and enjoy all the benefits of your new account:
                                                             <br><br>
                                                             <b>Set a Password:</b><br>
                                                             - To get started, simply click the button below to create a password for your account. This will ensure the security of your information and allow you to access your account at any time.<br>


                                                   </p>

                                                   <div>
                                                      <div style="padding-top:16px;padding-bottom:16px;text-align:left">

                                                         <div style="padding-bottom:15px;text-align:center">

                                                            <tr align="center">
                                                               <td style="width:100%;height:5px"></td>
                                                            </tr>



  <!-- BUTTON                                                            -->
<table border="0" width="100%" cellspacing="0" cellpadding="0" style="border-collapse:collapse">
   <tbody>
      <tr>
         <td height="2" style="line-height:2px">&nbsp;</td>
      </tr>
      <tr>
         <td align="middle">
            <a href="http://{SITE_DOMAIN}/reset-password?code={self.kwargs['code']}&user={self.kwargs['user_uuid']}" style="color:#01344B;text-decoration:none" rel="noreferrer" target="_blank" >
               <table border="0" width="100%" cellspacing="0" cellpadding="0" style="border-collapse:collapse">
                  <tbody>
                     <tr>
                        <td style="border-collapse:collapse;border-radius:6px;text-align:center;display:block;background:#01344B;padding:8px 16px 10px 16px">
            <a href="http://{SITE_DOMAIN}/reset-password?code={self.kwargs['code']}&user={self.kwargs['user_uuid']}" style="color:#01344B;text-decoration:none;display:block" rel="noreferrer" target="_blank" ><center><table border="0" cellspacing="0" cellpadding="0" style="border-collapse:collapse"><tbody><tr align="center"><td style="padding-top:6px"></td><td><font size="3"><span style="font-family:Helvetica Neue,Helvetica,Lucida Grande,tahoma,verdana,arial,sans-serif;white-space:nowrap;font-weight:bold;vertical-align:middle;color:#ffffff;font-weight:500;font-family:Roboto-Medium,Roboto,-apple-system,BlinkMacSystemFont,Helvetica Neue,Helvetica,Lucida Grande,tahoma,verdana,arial,sans-serif;font-size:14px;line-height:14px; text-align: center !important;">Set A Password</span></font></td></tr></tbody></table></center></a></td></tr></tbody></table></a>
         </td>
      </tr>
      <tr>
         <td height="8" style="line-height:8px">&nbsp;</td>
      </tr>
      <tr>
         <td height="0" style="line-height:0px">&nbsp;</td>
      </tr>
   </tbody>
</table>





                                                         </div>
                                                      </div>

                                                   </div>


                                                </td>
                                             </tr>
                                             <tr align="center">
                                                <td style="width:100%;height:30px"></td>
                                             </tr>
                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                                 <tr align="center">
                                    <td style="width:100%;height:5px"></td>
                                 </tr>
                              </tbody>
                           </table>
                           <table style="width:100%" align="center">
                              <tbody>
                                 <tr align="center">
                                    <td>
                                       <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                                          <tbody>
                                             <tr align="center">
                                                <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#fbfbfc;padding:20px 0px 0px 0px;background-color:#e9ebee">
                                                   <div>
                                                      <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                         <tbody>
                                                            <tr align="center">
                                                               <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;color:#8f949b;font-size:12px;padding:0 20px">

                                                                  Trading Forex and CFDs involves significant risk and can result in the loss of your invested capital. You should not invest more than you can afford to lose and should ensure that you fully understand the risks involved. <br>
                                                                  *Past Performance does not guarantee future returns.

                                                                  </td>
                                                            </tr>
                                                            <tr align="center">
                                                               <td style="width:100%;height:15px"></td>
                                                            </tr>
                                                         </tbody>
                                                      </table>
                                                      <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                         <tbody>
                                                            <tr align="center">
                                                               <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;background-color:#979797;width:100%;height:1px"></td>
                                                            </tr>
                                                            <tr align="center">
                                                               <td style="width:100%;height:15px"></td>
                                                            </tr>
                                                         </tbody>
                                                      </table>
                                                   </div>
                                                   <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                      <tbody>
                                                         <tr align="center">
                                                            <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;color:#8f949b;font-size:12px;padding:0 64px">QtradeInvest Direct Investing<br>
                                                               700 - 1111 West Georgia Street<br>
                                                               Vancouver, BC V6E 4T6</td>
                                                         </tr>
                                                         <tr align="center">
                                                            <td style="width:100%;height:0"></td>
                                                         </tr>
                                                      </tbody>
                                                   </table>
                                                </td>
                                             </tr>

                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                              </tbody>
                           </table>
                        </td>
                     </tr>
                  </tbody>
               </table>
            </td>
         </tr>
         <tr align="center">
            <td style="width:100%;height:30px"></td>
         </tr>

      </tbody>
   </table>
</div>

            """
        elif self.reason == "otp":
            return f"""

            <div style="padding:0">
   <table align="center" style="background-color:#e9ebee;width:100%;max-width:100%;min-width:100%" border="0" cellpadding="0" cellspacing="0" width="100%">
      <tbody>
         <tr align="center">
            <td style="width:100%;height:20px"></td>
         </tr>
         <tr align="center">
            <td align="center">
               <table border="0" cellpadding="0" cellspacing="0" width="100%">
                  <tbody>
                     <tr>
                        <td>

                           <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                              <tbody>
                                 <tr align="center">
                                    <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#01344B;padding:0;background-color:#01344B">
                                       <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                          <tbody>
                                             <tr align="center">
                                                <td style="text-align:center;border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%"><img width="70" height="" src="https://iqtradepro.ca/static/img/logo-icon.png" style="border:0;max-width:100%" alt="Header" title="Image" class="CToWUd" data-bit="iit" jslog="138226; u014N:xr6bB; 53:WzAsMl0."></td>
                                             </tr>
                                             <tr align="center">
                                                <td style="width:100%;height:0"></td>
                                             </tr>
                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                                 <tr align="center">
                                    <td style="width:100%;height:21px"></td>
                                 </tr>
                              </tbody>
                           </table>
                           <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                              <tbody>
                                 <tr align="center">
                                    <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#fbfbfc;background-color:#ffffff">

                                       <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                          <tbody>
                                             <tr align="center">
                                                <td style="text-align:left;border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;font-family:SF Pro Text;font-size:15px;line-height:20px;letter-spacing:-0.24px;color:#050505">
                                                   Hi {self.kwargs['name']},

                                                   <p>
                                                      Use the code below to authenticate your request:

                                                   </p>
                                                   <p style="font-family: monospace; font-size: 1.3em">{self.kwargs['code']}</p>

                                                   <div>
                                                      <div style="padding-top:16px;padding-bottom:16px;text-align:left">

                                                         <div style="padding-bottom:15px;text-align:center">

                                                            <tr align="center">
                                                               <td style="width:100%;height:5px"></td>
                                                            </tr>




                                                         </div>
                                                      </div>

                                                   </div>


                                                </td>
                                             </tr>
                                             <tr align="center">
                                                <td style="width:100%;height:30px"></td>
                                             </tr>
                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                                 <tr align="center">
                                    <td style="width:100%;height:5px"></td>
                                 </tr>
                              </tbody>
                           </table>
                           <table style="width:100%" align="center">
                              <tbody>
                                 <tr align="center">
                                    <td>
                                       <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                                          <tbody>
                                             <tr align="center">
                                                <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#fbfbfc;padding:20px 0px 0px 0px;background-color:#e9ebee">
                                                   <div>
                                                      <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                         <tbody>
                                                            <tr align="center">
                                                               <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;color:#8f949b;font-size:12px;padding:0 20px">

                                                                  Trading Forex and CFDs involves significant risk and can result in the loss of your invested capital. You should not invest more than you can afford to lose and should ensure that you fully understand the risks involved. <br>
                                                                  *Past Performance does not guarantee future returns.

                                                                  </td>
                                                            </tr>
                                                            <tr align="center">
                                                               <td style="width:100%;height:15px"></td>
                                                            </tr>
                                                         </tbody>
                                                      </table>
                                                      <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                         <tbody>
                                                            <tr align="center">
                                                               <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;background-color:#979797;width:100%;height:1px"></td>
                                                            </tr>
                                                            <tr align="center">
                                                               <td style="width:100%;height:15px"></td>
                                                            </tr>
                                                         </tbody>
                                                      </table>
                                                   </div>
                                                   <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                      <tbody>
                                                         <tr align="center">
                                                            <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;color:#8f949b;font-size:12px;padding:0 64px">QtradeInvest Direct Investing<br>
                                                               700 - 1111 West Georgia Street<br>
                                                               Vancouver, BC V6E 4T6</td>
                                                         </tr>
                                                         <tr align="center">
                                                            <td style="width:100%;height:0"></td>
                                                         </tr>
                                                      </tbody>
                                                   </table>
                                                </td>
                                             </tr>

                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                              </tbody>
                           </table>
                        </td>
                     </tr>
                  </tbody>
               </table>
            </td>
         </tr>
         <tr align="center">
            <td style="width:100%;height:30px"></td>
         </tr>

      </tbody>
   </table>
</div>

            """
        elif self.reason == "reset_password":
            return f"""

            <div style="padding:0">
   <table align="center" style="background-color:#e9ebee;width:100%;max-width:100%;min-width:100%" border="0" cellpadding="0" cellspacing="0" width="100%">
      <tbody>
         <tr align="center">
            <td style="width:100%;height:20px"></td>
         </tr>
         <tr align="center">
            <td align="center">
               <table border="0" cellpadding="0" cellspacing="0" width="100%">
                  <tbody>
                     <tr>
                        <td>

                           <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                              <tbody>
                                 <tr align="center">
                                    <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#01344B;padding:0;background-color:#01344B">
                                       <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                          <tbody>
                                             <tr align="center">
                                                <td style="text-align:center;border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%"><img width="70" height="" src="https://iqtradepro.ca/static/img/logo-icon.png" style="border:0;max-width:100%" alt="Header" title="Image" class="CToWUd" data-bit="iit" jslog="138226; u014N:xr6bB; 53:WzAsMl0."></td>
                                             </tr>
                                             <tr align="center">
                                                <td style="width:100%;height:0"></td>
                                             </tr>
                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                                 <tr align="center">
                                    <td style="width:100%;height:21px"></td>
                                 </tr>
                              </tbody>
                           </table>
                           <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                              <tbody>
                                 <tr align="center">
                                    <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#fbfbfc;background-color:#ffffff">

                                       <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                          <tbody>
                                             <tr align="center">
                                                <td style="text-align:left;border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;font-family:SF Pro Text;font-size:15px;line-height:20px;letter-spacing:-0.24px;color:#050505">
                                                   Hi {self.kwargs['name']},

                                                   <p>
                                                      Almost done!<br>
                                                       To complete your password reset action, click on the button below
                                                   </p>

                                                   <div>
                                                      <div style="padding-top:16px;padding-bottom:16px;text-align:left">

                                                         <div style="padding-bottom:15px;text-align:center">

                                                            <tr align="center">
                                                               <td style="width:100%;height:5px"></td>
                                                            </tr>


<!-- BUTTON                                                            -->
<table border="0" width="100%" cellspacing="0" cellpadding="0" style="border-collapse:collapse">
   <tbody>
      <tr>
         <td height="2" style="line-height:2px">&nbsp;</td>
      </tr>
      <tr>
         <td align="middle">
            <a href="http://{SITE_DOMAIN}/reset-password?code={self.kwargs['code']}&user={self.kwargs['user_uuid']}" style="color:#01344B;text-decoration:none" rel="noreferrer" target="_blank" >
               <table border="0" width="100%" cellspacing="0" cellpadding="0" style="border-collapse:collapse">
                  <tbody>
                     <tr>
                        <td style="border-collapse:collapse;border-radius:6px;text-align:center;display:block;background:#01344B;padding:8px 16px 10px 16px">
            <a href="http://{SITE_DOMAIN}/reset-password?code={self.kwargs['code']}&user={self.kwargs['user_uuid']}" style="color:#01344B;text-decoration:none;display:block" rel="noreferrer" target="_blank" ><center><table border="0" cellspacing="0" cellpadding="0" style="border-collapse:collapse"><tbody><tr align="center"><td style="padding-top:6px"></td><td><font size="3"><span style="font-family:Helvetica Neue,Helvetica,Lucida Grande,tahoma,verdana,arial,sans-serif;white-space:nowrap;font-weight:bold;vertical-align:middle;color:#ffffff;font-weight:500;font-family:Roboto-Medium,Roboto,-apple-system,BlinkMacSystemFont,Helvetica Neue,Helvetica,Lucida Grande,tahoma,verdana,arial,sans-serif;font-size:14px;line-height:14px; text-align: center !important;">Reset Password</span></font></td></tr></tbody></table></center></a></td></tr></tbody></table></a>
         </td>
      </tr>
      <tr>
         <td height="8" style="line-height:8px">&nbsp;</td>
      </tr>
      <tr>
         <td height="0" style="line-height:0px">&nbsp;</td>
      </tr>
   </tbody>
</table>



                                                         </div>
                                                      </div>

                                                   </div>


                                                </td>
                                             </tr>
                                             <tr align="center">
                                                <td style="width:100%;height:30px"></td>
                                             </tr>
                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                                 <tr align="center">
                                    <td style="width:100%;height:5px"></td>
                                 </tr>
                              </tbody>
                           </table>
                           <table style="width:100%" align="center">
                              <tbody>
                                 <tr align="center">
                                    <td>
                                       <table align="center" style="max-width:600px;width:100%" cellpadding="0" cellspacing="0" border="0">
                                          <tbody>
                                             <tr align="center">
                                                <td style="max-width:600px;padding:50px 40px 40px 40px;width:100%;background-color:#fbfbfc;padding:20px 0px 0px 0px;background-color:#e9ebee">
                                                   <div>
                                                      <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                         <tbody>
                                                            <tr align="center">
                                                               <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;color:#8f949b;font-size:12px;padding:0 20px">

                                                                  Trading Forex and CFDs involves significant risk and can result in the loss of your invested capital. You should not invest more than you can afford to lose and should ensure that you fully understand the risks involved. <br>
                                                                  *Past Performance does not guarantee future returns.

                                                                  </td>
                                                            </tr>
                                                            <tr align="center">
                                                               <td style="width:100%;height:15px"></td>
                                                            </tr>
                                                         </tbody>
                                                      </table>
                                                      <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                         <tbody>
                                                            <tr align="center">
                                                               <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;background-color:#979797;width:100%;height:1px"></td>
                                                            </tr>
                                                            <tr align="center">
                                                               <td style="width:100%;height:15px"></td>
                                                            </tr>
                                                         </tbody>
                                                      </table>
                                                   </div>
                                                   <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:100%">
                                                      <tbody>
                                                         <tr align="center">
                                                            <td style="border-spacing:0;color:#4c4c4c;font-family:ArialMT,Arial,sans-serif;font-size:15px;width:100%;color:#8f949b;font-size:12px;padding:0 64px">QtradeInvest Direct Investing<br>
                                                               700 - 1111 West Georgia Street<br>
                                                               Vancouver, BC V6E 4T6</td>
                                                         </tr>
                                                         <tr align="center">
                                                            <td style="width:100%;height:0"></td>
                                                         </tr>
                                                      </tbody>
                                                   </table>
                                                </td>
                                             </tr>

                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                              </tbody>
                           </table>
                        </td>
                     </tr>
                  </tbody>
               </table>
            </td>
         </tr>
         <tr align="center">
            <td style="width:100%;height:30px"></td>
         </tr>

      </tbody>
   </table>
</div>

            """





