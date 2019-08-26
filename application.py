import os
import boto3
import datetime
import json
from requests_aws4auth import AWS4Auth
import requests
from flask import Flask
from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)

#Access information for AWS
region='us-east-1'
accessKey = os.environ['ACCESS_KEY']
secretKey = os.environ['SECRET_KEY']

application = Flask(__name__)

@application.route('/')
def members():
   return render_template('search_member.html', title='Member Search')


@application.route('/get', methods=['GET', 'POST'])
def get_member():

    #Get the member number from the Flask form
    if request.method == 'POST':
        phone_number = request.form['phone_number']

    #Get results from API
    result = callAPI('GET', {'phone_number': phone_number})

    #If the response is a string, it has not found the member
    if type(result) == str:
        response = "No member found matching those attributes"
    else:
        response = "Member Found"

    #If an attribute is not returned from the API, assign it the value of an empty string
    attr = ["address", "city", "dob", "doj", "first_name", "last_name", "gender", "state", "zip"]
    for item in attr:
        if type(result) != str:
            if item not in result:
                result[item] = ""

    if type(result) != str:
        return render_template('member.html',
            title='Member Data',
            name=result['first_name'] + " " + result['last_name'],
            address = result['address'],
            city = result['city'],
            state = result['state'],
            zip = result['zip'],
            dob=result['dob'],
            doj=result['doj'],
            gender=result['gender'],
            phone_number=result['phone_number'],
            response=response)
    else:
        return render_template('member.html',
            title='Member Not Found',
            response=response)



@application.route('/add', methods=['GET', 'POST'])
def add_member():

    #Get the current date and time
    now = datetime.datetime.now()

    #Initialize variable
    result = "Add a member"
    #Initialize dictionary to hold body of API call
    body = {}
    exists = "test"

    if request.method == 'POST':
            
            attrs = ['phone_number', 'first_name', 'last_name', 'address', 'city', 'state', 'zip', 'gender', 'phone_number', 'dob']

            for item in attrs:
                if request.form[item] != "":
                    body.update({item:request.form[item]})

            body.update({'doj': now.strftime("%Y-%m-%d")})

            if request.form['phone_number'] == "":
                result = "You must enter a phone number"
            else:
                phone_number = request.form['phone_number']
                exists = callAPI('GET', {'phone_number': phone_number})

                if type(exists) != str:
                    result = "A member with these attributes already exists."
                else:
                    result = callAPI('POST', body)
                    result = result['message']
            
    return render_template('add_member.html',
        title='Add Member',
        result = result,
        exists=exists)

@application.route('/delete', methods=['POST', 'GET'])
def delete_member():

    result = "Enter a phone number to delete the member"

    if request.method == 'POST':

        phone_number = request.form['phone_number']
        exists = callAPI('GET', {'phone_number': phone_number})

        if type(exists) == str:
                    result = "No member with that data exists to delete"
        else:
            phone_number = request.form['phone_number']
            #Get results from API
            result = callAPI('DELETE', {'phone_number': phone_number})

    return render_template('delete_member.html',
        title='Delete Member',
        result = result)


def callAPI(method, body):

    region = 'us-east-1'
    service = 'execute-api'
    auth = AWS4Auth(accessKey, secretKey, region, service)
    headers = {}
    body = body #This is the json data that is sent to the API & Lambda function as the "event" parameter.
    method = method
    url = 'https://8qtq3iaicd.execute-api.us-east-1.amazonaws.com/Dev/members'

    response = requests.request(method, url, auth=auth, data=json.dumps(body), headers=headers)
    return(json.loads(response.text))



if __name__ == '__main__':
    application.debug = False
    application.run()