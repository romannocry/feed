Generator.py
This function is an add-on to the email function

Generator function's goal is to take a json payload and generate a html table widget that will be embedded in emails:

Default urls:
receiver's web page: https://loop.email/receiver
receiver's function: https://lambdda/receiver

Example output
<table>
<tr>
<td><a href="https://loop.email/receiver/{b64payload}"></td> //yes
<td><a href="https://loop.email/receiver/{b64payload}"></td> //no
</tr>
</table>

What happens when user clicks on yes:
1. user is redirected to https://loop.email/receiver/{b64payload}
2. receiver function decodes b64payload
3. receiver function stores the input in the storage url if provided
4. receiver function redirects user to redirect url if provided
5. receiver function triggers the api with the params if provided
6. user lands on the redirect url
