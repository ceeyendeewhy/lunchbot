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
    for x in signups:
        if x == user:
            return False
    signups.append(user)
    return True

def createGroup(userA, userB, userC):
    group = slack_client.api_call("mpim.open", token=os.environ.get('SLACK_BOT_TOKEN'), users=userA + "," + userB + "," + userC + "," + BOT_ID)
    slack_client.api_call("chat.postMessage", channel=group['group']['id'],
        text="Let's get lunch!", as_user=True)

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
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


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