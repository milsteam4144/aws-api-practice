# aws-api-practice
Simple Flask Application to test connecting/making calls to a REST API using AWS API Gateway, Lambda Functions and DynamoDB.

LINK: http://flask-env.hapfgbxpnf.us-east-1.elasticbeanstalk.com/add

To test functionality:

-Visit link "Add Member"
   -Add a member: must include phone number(in format XXX-XXX-XXXX), last name and first name

-Visit link "Search for a Member"
   -Input the phone number (in the same format) that you just used to add the member
   -You should see any information you entered about the user
   -If the phone number is incorrect you will see a message that the user does not exist.

-Visit the link "Delete a Member"
   -Enter the phone number of the member that you wish to delete
   -You will get a success message

-Visit the link "Search for a Member"
   -Try to search for the phone number of the member you just deleted
   -You should receive a message that the member does not exist.


*The image file db_screenshot contains "dummy data" of members with corresponding phone numbers. This data can be used for testing purposes

*The folder lambda_functions contains the lambda functions that are hosted on AWS. These functions are invoked by calls to the API.


***Tasks to implements in the future***
-Implement "UPDATE" API call to update member data
-Implement AWS Cognito to authenticate and authorize users to access application/API
-Use DynamoDB/S3 to upload and return images of users
-Improve visuals of web application (HTML/CSS)
