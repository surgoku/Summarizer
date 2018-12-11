from __future__ import print_function
import csv
import random
import wikipedia
import boto3
import datetime

# dict for fact
dict_opinion = {}
dict_news = {}
dict_facts = {}

# Readinf opinion file
with open('topic_summaries_opinion_output.csv', 'r', encoding='utf8') as f:
    reader1 = csv.reader(f)
    opinion_list = list(reader1)

# Reading fact file
with open('topic_summaries_fact_output.csv', 'r', encoding='utf8') as f:
    reader2 = csv.reader(f)
    facts_list = list(reader2)

# Reading news file
with open('topic_summaries_news_output.csv', 'r', encoding='utf8') as f:
    reader3 = csv.reader(f)
    news_list = list(reader3)


# Extract topics from document and saving into dictionary
def add_to_dict(document_list, dic_file):
    num = 0
    for i in range(len(document_list)):
        dic_file[document_list[i][1]] = num
        num += 1


# adding values to dictionary
# add_to_dict(opinion_list, dict_opinion)
num, num1, num2 = 0, 0, 0
for i in range(len(opinion_list)):
    dict_opinion[opinion_list[i][1]] = num
    num += 1

# add_to_dict(facts_list, dict_facts)
for i in range(len(facts_list)):
    dict_facts[facts_list[i][1]] = num1
    num1 += 1

# add_to_dict(news_list, dict_news)
num2 = 0
for i in range(len(news_list)):
    dict_news[news_list[i][1]] = num2
    num2 += 1

num, num1, num2 = 0, 0, 0


# Extracting summary
def extract_summary(slot_value, name_of_intent):
    # if slot_value in dict_facts or slot_value in dict_news or slot_value in dict_opinion:
    if 1 == 1:
        # if slot value in dicionary then
        if name_of_intent == "facts":
            dicionary_to_use = dict_facts
            name_of_intent = facts_list
        elif name_of_intent == "news":
            dicionary_to_use = dict_news
            name_of_intent = news_list
        elif name_of_intent == "opinion":
            dicionary_to_use = dict_opinion
            name_of_intent = opinion_list
        list_5_summaries = []
        for i in range(2, 7):
            list_5_summaries.append(name_of_intent[dicionary_to_use[slot_value]][i])
        random_number = random.randint(0, 4)
        if not list_5_summaries[random_number]:
            return ""
        else:
            return list_5_summaries[random_number]
    # else go to wiki
    else:
        summary_wikipedia = str(wikipedia.summary(slot_value))
        stop = "."
        count = 0
        result = ""
        for i in range(len(summary_wikipedia)):
            if summary_wikipedia[i] == stop:
                count += 1
            result += summary_wikipedia[i]
            if count == 2:
                break
        return result


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


def dialog_response(attributes, endsession):
    """  create a simple json response with card """
    return {
        'version': '1.0',
        'sessionAttributes': attributes,
        'response': {
            'directives': [
                {
                    'type': 'Dialog.Delegate'
                }
            ],
            'shouldEndSession': endsession
        }
    }


# --------------- Functions that control the skill's behavior ------------------
def get_test_response():
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    session_attributes = {}
    card_title = "Test"
    speech_output = "This is a test message"
    reprompt_text = "You never responded to the first test message. Sending another one."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to your custom alexa application!"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I don't know if you heard me, welcome to your custom alexa application!"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts.
        One possible use of this function is to initialize specific
        variables from a previous state stored in an external database
    """
    # Add additional code here as needed
    pass


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    # Dispatch to your skill's launch message
    return get_welcome_response()


def on_intent(intent_request, session):
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "How can i help you?"
    reprompt_text = "Hello are you there?"
    should_end_session = False
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    # to_search = "Obama"
    slot_variable = ""

    # Dispatch to your skill's intent handlers
    if intent_name == "news":
        slot_variable = intent["slots"]["Name"]["value"]
        ####################### Mycode
        return build_response(session_attributes, build_speechlet_response(
            card_title, extract_summary(slot_variable, intent_name), reprompt_text, should_end_session))
        ########

        return build_response(session_attributes, build_speechlet_response(
            card_title, extract_summary(slot_variable, intent_name), reprompt_text, should_end_session))
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    elif intent_name == "facts":
        slot_variable = intent["slots"]["Name"]["value"]
        return build_response(session_attributes, build_speechlet_response(
            card_title, extract_summary(slot_variable, intent_name), reprompt_text, should_end_session))
    elif intent_name == "opinion":
        slot_variable = intent["slots"]["Name"]["value"]
        return build_response(session_attributes, build_speechlet_response(
            card_title, extract_summary(slot_variable, intent_name), reprompt_text, should_end_session))
    # For the feedback
    elif intent_name == "feedback":
        rating = intent["slots"]["Number"]["value"]
        ############ for dynamo db
        client = boto3.client('dynamodb')
        table = boto3.resource('dynamodb').Table('Feedback')
        table.put_item(Item={
            'Date': str(datetime.datetime.now()), 'Rating': rating
        })

        if int(rating) in [0, 1, 2, 3, 4, 5]:
            client = boto3.client('dynamodb')
            table = boto3.resource('dynamodb').Table('Feedback')
            table.put_item(Item={
                'Date': str(datetime.datetime.now()), 'Rating': rating
            })
            return build_response(session_attributes, build_speechlet_response(
                card_title, "Thank you for your feedback! Have a great day.", reprompt_text, should_end_session))
        else:
            return build_response(session_attributes, build_speechlet_response(
                card_title, "Sorry! That's an invalid response. Did you make sure to use a rating between 0 to 5?",
                reprompt_text, should_end_session))
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("Incoming request...")

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])