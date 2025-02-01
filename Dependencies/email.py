import sib_api_v3_sdk 
from sib_api_v3_sdk.rest import ApiException
import os
from dotenv import load_dotenv

load_dotenv()

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = os.getenv('brevo')
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

def sendEmailResults(rslt):
    if len(rslt.message_id) == 0:
        return False
    else:
        return True
    

def sendEmail(Subject, To, Template_id, code = None):
    # perpose : send email 
    # response : true : successfull || false : failed
    subject = Subject
    sender = {"name":"Administration account creation","email":"gayashan.randimagamage@gmail.com"}
    to = [{"email": To ,"name": 'dummy name'}]
    headers = {"Some-Custom-Name":"unique-id-1234"}
    if code != None:
        # with secreate code
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, sender=sender, subject=subject, template_id= Template_id, params= code)
        api_response = api_instance.send_transac_email(send_smtp_email)
        return sendEmailResults(api_response)
    elif code == None:
        # without secreate code
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, sender=sender, subject=subject, template_id= Template_id)
        api_response = api_instance.send_transac_email(send_smtp_email)
        return sendEmailResults(api_response)
