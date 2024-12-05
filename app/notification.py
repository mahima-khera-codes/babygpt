from app.slack.model.construct_payload import contruct_payload_from_request
from app.slack.model.validate_message import validate_message
from app.slack.model.construct_message import fetch_user_details
from app.slack.model.construct_message import construct_message


#==========Base class for send notification to slack,email and by zapier to any system=========
#==========I followed the same app factory pattren https://realpython.com/factory-method-python/#the-problems-with-complex-conditional-code
#==========I did some minor changes in our system functions==============
    #1. Like these all functions were calling from notify/dispatch api before.
    #2. So our tms cron was hit dispatch api and api was calling contruct_payload_from_request function and //
    #   inside the same function all functions were calling without return call one by one
    #3. I did change remove inside calling functions and add return values there so we can use here functions


#Base class for functions used for notification 
class notify_system:

    #1.This first function which will be call from notify/dispatch api.
    #2.This function will just give us message from message_details which user send in request.
    #3.this function same for any request slack,email or zapier or enything else this will call for every
    #4.Input : message_details,user json request...
    #5.Output : will return message with variables next step will be get message variables so will call another function
    #If everything available in request then it will return proper output else will raise exception
    def make_payload_from_request(self,account_name,mongo,message_detail,input):
        message,message_detail,req_json = contruct_payload_from_request(message_detail=message_detail,input=input)
        return self.message_variables_validation(account_name,message,message_detail,req_json,mongo)

    #1.This function will call from first function from there we got message now will get message variables from message.
    #2.In this function we will get message and system variables which will replace by actual value.
    #3.This function will also call for every request itself
    #4.Input:message,message_detail,req_json
    #5.Output: message_variables,system_require
    #If everything available in request then it will return proper output else will raise exception
    def message_variables_validation(self,account_name,message,message_detail,req_json,mongo):
        message,message_variables,req_json,system_require,message_detail = validate_message(message,req_json,message_detail)
        return self.get_user_details(account_name,message,req_json,message_variables,system_require,message_detail,mongo)

    #1.This function used for just dump the user details request.
    #2.Input: jsonrequest
    #3.Output: userdetails json dump
    def get_user_details(self,account_name,message,req_json,message_variables,system_require,message_detail,mongo):
        user_slack_details,user_email_details,user_zapier_details = fetch_user_details(req_json)
        return self.construct_message_in_database(account_name,user_slack_details,user_email_details,user_zapier_details,message,req_json,message_variables,system_require,message_detail,mongo)

    #1.This is the mail function which will insert message request into collection.
    #2.This function first will check for which platform message requested.
    #3.If request for zapier it will hit zapier function and will insert zapier request in collection.
    #4.If request for slack it will hit slack function and will insert slack request in collection.
    #5.If request for email it will hit email function and will insert email request in collection.
    #6.If request for any off two it will insert request for both.
    #7.In these all there systems a common function used for message making "make message" it will create message by request accordingly if request for slack message will make with tag else with name
    #8.Not sure only about this function if anything need to change in this
    def construct_message_in_database(self,account_name,user_slack_details,user_email_details,user_zapier_details,message,req_json,message_variables,system_require,message_detail,mongo):
        return construct_message(account_name,user_slack_details,user_email_details,user_zapier_details,message,req_json,message_variables,system_require,message_detail,mongo)


#===============This class function work only insert message request in message_cron collection according to platform.======
#=========For send notification there is another story from starting of notification system.==========
#Now we have message message reuqest in collection with message details where it will go,message,subject,from,to,channel etc.
#We have a cron which will take requests from db and send notification one by one.