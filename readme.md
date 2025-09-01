Generator.py
This function is an add-on to the email function. It creates a table inside the email that contains actions that are encoded in b64.

Receiver.py
This function processes the 

Generator function's goal is to take a json payload and generate a html table widget that will be embedded in emails:

Default urls:
receiver's web page: https://loop.email/receiver
receiver's function: https://lambdda/receiver



How to create a notification
```
{
  "uuid": "string", 
  "loggingEmailGeneration": true,
  "campaignName": "Deal Status Update",
  "creator": "test@gmail.com",
  "to": ["user1@example.com", "user2@example.com"],
  "from": "system",
  "subject": "Deal 123 - Update your deal status",
  "title": "Deal Status Update",
  "subtitle": "Please update the status of your deal",
  "structure": [
    {
      "type": "text",
      "body": "<h1>Deal Status Update</h1><p>Please update the status of your deal.</p>"
    },
    {
      "type": "button",
      "body": "<a>Click here to update your deal status</a>"
    },
    {
      "type": "actions_table",
      "body": {
        "uuid": "string",
        "validators": ["user1@example.com", "user2@example.com"],
        "table_orientation": "vertical",
        "default_settings": {
          "storage": "https://lambda/db/123",
          "key": "Status"
        },
        "options": [
          {
            "value": "Won",
            "triggerOnSuccess": {
              "api": "https://api/updateDealStatus",
              "method": "POST",
              "params": {
                "status": "Won",
                "dealId": "123"
              }
            }
          },
          {
            "value": "Lost",
            "triggerOnSuccess": {
              "api": "https://api/updateDealStatus",
              "method": "POST",
              "params": {
                "status": "Lost",
                "dealId": "123"
              }
            }
          }
        ],
        "context": {
          "id": 123,
          "name": "Deal 123",
          "owner_email": "test@gmail.com"
        }
      }
    },
    {
      "type": "image",
      "body": "https://placekitten.com/200/300"
    },
    {
      "type": "footer",
      "body": "<p>Thank you for using our service!</p>"
    }
  ]
}
```

Flow

1. user is redirected to https://loop.email/receiver/{b64payload}
2. receiver function decodes b64payload
3. receiver function stores the input in the storage url if provided
4. receiver function redirects user to redirect url if provided
5. receiver function triggers the api with the params if provided
6. user lands on the redirect url
