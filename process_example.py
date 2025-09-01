from generator import generate_actions_table
from helpers import generate_uuid
import datetime
from notification import notification as NotificationLog

#client id will have to have write access to the db
#Attributes needed to set-up a process
storage_db_url = "https://lambda/db/"
storage_table_name = "table"
email_generator_function_uri = "lambda/function/email_generator"

#mock function to simulate the process
def trigger_email_function(notification_structure):
    print(f"Triggering email function")
    #for test only, in prod this will be a call to the email template function
    generate_actions_table(**notification_structure["structure"][2]["body"])
    loggingEmailGeneration = notification_structure.get("loggingEmailGeneration", True)
    if loggingEmailGeneration:
        log = NotificationLog(
            uuid=notification_structure["uuid"],
            campaignName=notification_structure["campaignName"],
            creator=notification_structure["creator"],
            to=notification_structure["to"],
            from_=notification_structure["from"],
            creation_date=int(datetime.datetime.now().timestamp())
        )
        print("Logging email generation:", log.to_csv_row())
        
def example_process():
    default_settings = {
        # default settings that can be overridden by the options payload
        "storage": storage_db_url + storage_table_name,
        #"redirect": "https://www.google.com",
        #the key is the attribute name of the value in the option payload
        "key": "Status"
        
    }
    options_payload = [
        {
            "value":"Won, you're good!",
            "triggerOnSuccess": {
                #currently, the thought is to leverage our client id/client secret to call the api
                #but it could become a parameter in the future but cannot be passed in the email for security reasons
                "api": "https://api/updateDealStatus",
                "scope": "write:deals",
                "method": "POST",
                "params": {
                    "status": "won",
                    "dealId": "{{bdrId.id.ref}}"
                }
            }
        },
        {
           "value":"Lost, too bad..",
           "triggerOnSuccess": {
               "api": "https://api/updateDealStatus",
                "scope": "write:deals",
               "method": "POST",
               "params": {
                   "status": "lost",
                   "dealId": "{{deal.id}}"
               }
           }
        },
    ]

    deals = [
        {"bdrId":{"id":{"ref":1234,"test":"test"},"label":"ABC"},"id":1, "name":"Deal 1", "owner_email":"test@gmail.com"},
        #{"bdrId":{"id":{"ref":1234,"test":"test"},"label":"ABC"},"id":1, "name":"Deal 2", "owner_email":"test2@gmail.com"},
    ]

    for deal in deals:
        print(f"Processing deal: {deal}")
        uuid = generate_uuid()
        to_addr = [deal["owner_email"]]

        notification_structure = {
            "uuid":uuid,
            #loggingEmailGeneration is optional, default is true, if false, no logs are kept of the generation
            "loggingEmailGeneration": True,
            "campaignName":"Deal Status Update",
            "creator":"test@gmail.com",
            "to":to_addr,
            "from":"system",
            "subject":deal["name"] + " - Update your deal status",
            "title":"Deal Status Update",
            "subtitle":"Please update the status of your deal",
            "structure":[
                {"type":"text","body":"<h1>Deal Status Update</h1><p>Please update the status of your deal.</p>"},
                {"type":"button","body":"<a>Click here to update your deal status</a>"},
                #{"type":"actions_table","body":generate_actions_table(uuid=uuid,validators=to_addr,table_orientation='vertical',default_settings=default_settings,options=options_payload,context=deal)},
                {"type":"actions_table","body":{
                    "uuid":uuid,
                    "validators":to_addr,
                    "table_orientation":'vertical',
                    "default_settings":default_settings,
                    "options":options_payload,
                    "context":deal
                    }
                },

                {"type":"image","body":"https://placekitten.com/200/300"},
                {"type":"footer","body":"<p>Thank you for using our service!</p>"}
                ]
        }
        #send_to_email_template_function(generate_actions_table(sender=from_addr,recipients=to_addr,options=options_payload,params=deal))
        trigger_email_function(notification_structure)


if __name__ == "__main__":
    example_process()
