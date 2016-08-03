import os
import time
from slackclient import SlackClient

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">:"
EXAMPLE_COMMAND = "do"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

signups = []

# Adds the current user to the list
# Returns true if the user was not already in the list, false otherwise
def addToSignups(user):
    if user in signups:
        return False
    signups.append(user)
    return True

def createGroup(userA, userB, userC):
    userList = userA + "," + userB + "," + userC + "," + BOT_ID
    group = slack_client.api_call("mpim.open", token = os.environ.get('SLACK_BOT_TOKEN'), users = userList)
    slack_client.api_call("chat.postMessage", channel = group['group']['id'],
        text = "Let's get lunch!", as_user = True)

def handle_command(command, channel, user):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "hi"
    if command.startswith("cindy"):
        response = "Cindy Liu Who"
    if command.startswith("amy"):
        response = "Amy Hu is my grandma"
    if command.startswith("edward"):
        response = "You mean 'Eecsward'?"
    if command.startswith("satoko"):
        response = "You mean sugar child?"
    if command.startswith("alex"):
        response = "You mean Ryan."
    if command.startswith("ryan"):
        response = "You mean Alex..."
    if command.startswith("kira"):
        response = "is the Baum"
    if command.startswith("brittany"):
        response = "is brave."
    if command.startswith("lucy"):
        response = "is the owner of a minivan from Minnesota"
    if command.startswith("scott"):
        response = "aka Sean aka Sebastian aka Seamus aka Simon aka S*"
    if command.startswith("brandon"):
        response = "Where is your desk?"
    if command.startswith("dinesh"):
        response = "aka Simon 2.0"
    if command.startswith("amit"):
        response = "is a mitt"
    if command.startswith("signup"):
        response = "You've been added to the list!"
        if (addToSignups(user)):
            if (len(signups) >= 3):
                createGroup(signups.pop(), signups.pop(), signups.pop())
                response = "You've been added to the list! Creating a group chat for your lunch buddies now..."
            else:
                response = "You've been added to the list! Waiting for enough people to sign up for lunch..."
        else:
            response = "You're already in the list!"
    if command.startswith("remove"):
        if user in signups:
            response = "You've been removed from the list!"
            signups.remove(user)
        else:
            response = "You weren't already in the sign-up list!"
    if command.startwith("schedule")
        meetingData = parseData(command, channel)
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

# 
def parseData(command, channel):
    data = { "people" : [],
                "month" = date.month, 
                "day" = date.day, 
                "year" = date.year, 
                "time" = time.localtime(), 
                "duration" = 60,
                "purpose" = "Meeting" }
    return data

# Returns the people in the meeting
def parsePeople(channel):
    message = "Who do you want to invite to this meeting? \n" +
        "Please enter a list of people using their Adaptive usernames, separated by spaces: \n" +
        "Example: jdoe fbar"
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=message, as_user=True)
    input, _, _ = parse_slack_output(slack_client.rtm_read())
    return input.split(" ")

# Returns the date of the meeting
def parseDate(channel):
    message = "What day do you want to hold this meeting? \n" +
        "Please use MM/DD/YYYY format: \n" +
        "Example: 03/17/2016 for March 17, 2016"
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=message, as_user=True)
    input, _, _ = parse_slack_output(slack_client.rtm_read())
    date = input.split("/")
    return date[1], date[2], date[3]

# Returns the time of the meeting
def parseTime(channel):
    message = "What time do you want to hold this meeting? \n" +
        "Please \n" +
        "Example: "
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=message, as_user=True)
    input, _, _ = parse_slack_output(slack_client.rtm_read())

# Returns the duration of the meeting in minutes
def parseDuration(channel):
    message = "How long will this meeting be? \n" +
        "Please enter the duration in terms of hours: \n" +
        "Example: \"1.5\" for 1 hour and 30 minutes"
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=message, as_user=True)
    input, _, _ = parse_slack_output(slack_client.rtm_read())
    return input

# Returns the subject of the meeting to be scheduled
def parsePurpose(channel):
    message = "What is the topic of this meeting? \n" +
        "Example: "
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=message, as_user=True)
    input, _, _ = parse_slack_output(slack_client.rtm_read())
    return input

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel'], output['user']
    return None, None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel, user = parse_slack_output(slack_client.rtm_read())
            if command and channel and user:
                handle_command(command, channel, user)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")