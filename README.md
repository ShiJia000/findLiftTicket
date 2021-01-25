# findLiftTicket

This script is used to find lift tickets for Stevens Pass. You can use this script by either playing sound by your 
computer or sending email through AWS. If you want to use the sending email functionality, you need to have the AWS 
account ACCESS_KEY and SECRET_KEY.

Dependencies for sending emails:
1. AWS Simple Email Service
2. Python selenium library

Requires for sending emails:
1. AWS account ACCESS_KEY and SECRET_KEY

Command
``` python
# Only play sound from computer:
python main.py 01/01/2021

# send email:
python main.py 01/01/2021 abc@gmail.com
```
