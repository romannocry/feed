from generator import generate_actions_table
import uuid


email_template_function_uri = "lambda/trigger_email_template"

#send_to_email_template_function = lambda email_structure: print(f"Sending to {email_template_function_uri} with structure: {email_structure}")
send_to_email_template_function = lambda email_structure: print(email_structure)

def generate_uuid():
    return str(uuid.uuid4())

def example_process():
    # Example process
    # 1. dev pulls data from any api (exemple: active deals) - for all active deals, he wants to:
        #1.1 send an email to the deal owner to notify them that the deal is still active
        #1.2 send an email to the deal owner with a link to update the deal status
        #1.3 send an email to the deal owner with options to update the deal status (won, lost, in progress)

    #"loggingGeneration": True
    storage_uri = "https://lambda/db/123"

    default_settings = {
        # default settings that can be overridden by the options payload
        "storage": storage_uri,
        "redirect": "https://www.google.com",
        
    }
    options_payload = [
        {
            "label":"Won",
            "triggerOnSuccess": {
                "api": "https://api/updateDealStatus",
                "method": "POST",
                "params": {
                    "status": "won",
                    "dealId": "{{bdrId.id.ref}}"
                }
            }
        },
        {
           "label":"Lost",
           "triggerOnSuccess": {
               "api": "https://api/updateDealStatus",
               "method": "POST",
               "params": {
                   "status": "lost",
                   "dealId": "{{deal.id}}"
               }
           }
        },
        #{
        #    "label":"In Progress",
        #    "triggerOnSuccess": {
        #        "api": "https://api/updateDealStatus",
        #        "method": "POST",
        #        "params": {
        #            "status": "in_progress",
        #            "dealId": "{{deal.id}}"
        #        }
        #    }
        #}
    ]

    deals = [
        {"bdrId":{"id":{"ref":1234,"test":"test"},"label":"ABC"},"id":1, "name":"Deal 1", "owner_email":"test@gmail.com"},
        #{"id":2, "name":"Deal 2", "owner_email":"test2@gmail.com"},
        #{"id":3, "name":"Deal 3", "owner_email":"test3@gmail.com"},
    ]
    # 2. for each deal, generate the email structure and send it to the email template function 

    from_addr = "system"

    for deal in deals:
        print(f"Processing deal: {deal}")
        uuid = generate_uuid()
        to_addr = [deal["owner_email"]]

        email_structure = {
            "uuid":"unique-id-1234",
            "to":to_addr,
            "from":"system",
            "subject":deal["name"] + " - Update your deal status",
            "title":"Deal Status Update",
            "subtitle":"Please update the status of your deal",
            "structure":[
                {"type":"text","body":"<h1>Deal Status Update</h1><p>Please update the status of your deal.</p>"},
                {"type":"button","body":"<a>Click here to update your deal status</a>"},
                {"type":"actions_table","body":generate_actions_table(uuid=uuid,validators=to_addr,table_orientation='vertical',default_settings=default_settings,options=options_payload,context=deal)},
                {"type":"image","body":"https://placekitten.com/200/300"},
                {"type":"footer","body":"<p>Thank you for using our service!</p>"}
                ]
        }
        #send_to_email_template_function(generate_actions_table(sender=from_addr,recipients=to_addr,options=options_payload,params=deal))



if __name__ == "__main__":
    example_process()
