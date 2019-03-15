import datetime


# Here we define our Lambda function and configure what it does when
# an event with a Launch, Intent and Session End Requests are sent. # The Lambda function responses to an event carrying a particular
# Request are handled by functions such as on_launch(event) and
# intent_scheme(event).

def lambda_handler(event, context):
    if event['session']['new']:
        on_start()
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event)
    elif event['request']['type'] == "IntentRequest":
        return intent_scheme(event)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_end()

def on_start():
    print("Session Started.")

def on_launch(event):
    onlunch_MSG = "Hi, welcome to the Bus Mate Alexa Skill."
    reprompt_MSG = "This is the launch reprompt."
    card_TEXT = "Bus mate launch text"
    card_TITLE = "Bus Mate Launch Title"
    return output_json_builder_with_reprompt_and_card(onlunch_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

def on_end():
    print("Session Ended.")


# The intent_scheme(event) function handles the Intent Request.
# Since we have a few different intents in our skill, we need to
# configure what this function will do upon receiving a particular
# intent. This can be done by introducing the functions which handle
# each of the intents.

def intent_scheme(event):

    intent_name = event['request']['intent']['name']

    if intent_name == "nextTwoBuses":
        return next_two_buses(event)
    elif intent_name in ["AMAZON.NoIntent", "AMAZON.StopIntent", "AMAZON.CancelIntent"]:
        return stop_the_skill(event)
    elif intent_name == "AMAZON.HelpIntent":
        return assistance(event)
    elif intent_name == "AMAZON.FallbackIntent":
        return fallback_call(event)

def next_two_buses(event):
    line = event['request']['intent']['slots']['line']['value']
    stop = event['request']['intent']['slots']['stop']['value']
    direction = event['request']['intent']['slots']['direction']['value']
    print("Line Variable: {line}".format(line=line))
    print("Stop Variable: {stop}".format(stop=stop))
    print("Direction Variable: {direction}".format(direction=direction))
    now = datetime.datetime.now() - datetime.timedelta(hours = 4)
    print(now)
    schedule_type = get_schedule_type(now)
    schedule = BUS_SCHEDULE[line][stop][direction][schedule_type]
    print(len(schedule))

    next_two_buses = get_next_two_buses(now, schedule)

    response_text = get_response_text(next_two_buses)
    outputSpeech_text = response_text
    card_text = response_text
    card_title = 'Bus Mate'
    reprompt_text = 'This is our reprompt text'
    value = True

    return output_json_builder_with_reprompt_and_card(outputSpeech_text, card_text, card_title, reprompt_text, value)

def get_response_text(next_two_buses):
    if len(next_two_buses) == 2:
        bus_time_one = next_two_buses[0].strftime("%I:%M")
        bus_time_two = next_two_buses[1].strftime("%I:%M")
        return 'The next two buses are at {bus_time_one} and {bus_time_two}'.format(bus_time_one=bus_time_one, bus_time_two=bus_time_two)

    elif len(next_two_buses) == 1:
        bus_time_one = next_two_buses[0].strftime("%I:%M")
        return 'Theres only one bus at {bus_time_one}'.format(bus_time_one=bus_time_one)

    elif len(next_two_buses) == 0:
        return 'There are no more buses today. Walk bitch!'

    return 'fuck some shit broke'

def get_schedule_type(now):

    date_schedule = None
    weekday = now.weekday()
    if weekday < 5:
        date_schedule = DATE_WEEKDAY
    elif weekday == 5:
        date_schedule = DATE_SATURDAY
    elif weekday == 6:
        date_schedule = DATE_SUNDAY

    return date_schedule

def get_next_two_buses(now, schedule):
    current_time = now.time()
    print("We in get_next_two_buses")

    next_two_buses = []
    index = 0
    bus_time_count = 0
    print('Attempting to enter the while loop')
    print('index: {index}  length of schedule: {length}'.format(index=index, length=len(schedule)))
    print('Index Conditional: {}'.format(index < len(schedule)))
    print('bus_time_count: {}'.format(bus_time_count))
    print('Bus Count Conditional: {}'.format(bus_time_count < 2))
    print("While Conditional Met:{}".format((index < len(schedule)) & (bus_time_count < 2)))

    while (index < len(schedule)) & (bus_time_count < 2):
        print('Successfully entered while loop')
        schedule_time = schedule[index]
        print(schedule_time)
        print(current_time)
        print(schedule_time > current_time)
        if schedule_time > current_time:
            next_two_buses.append(schedule_time)
            bus_time_count = bus_time_count + 1

        index = index + 1
    print("Leaving get_next_two_buses")
    return next_two_buses


# The response of our Lambda function should be in a json format.
# That is why in this part of the code we define the functions which
# will build the response in the requested format. These functions
# are used by both the intent handlers and the request handlers to
# build the output.

def plain_text_builder(text_body):
    text_dict = {}
    text_dict['type'] = 'PlainText'
    text_dict['text'] = text_body
    return text_dict

def reprompt_builder(repr_text):
    reprompt_dict = {}
    reprompt_dict['outputSpeech'] = plain_text_builder(repr_text)
    return reprompt_dict

def card_builder(c_text, c_title):
    card_dict = {}
    card_dict['type'] = "Simple"
    card_dict['title'] = c_title
    card_dict['content'] = c_text
    return card_dict

def response_field_builder_with_reprompt_and_card(outputSpeech_text, card_text, card_title, reprompt_text, value):
    speech_dict = {}
    speech_dict['outputSpeech'] = plain_text_builder(outputSpeech_text)
    speech_dict['card'] = card_builder(card_text, card_title)
    speech_dict['reprompt'] = reprompt_builder(reprompt_text)
    speech_dict['shouldEndSession'] = value
    return speech_dict

def output_json_builder_with_reprompt_and_card(outputSpeech_text, card_text, card_title, reprompt_text, value):
    response_dict = {}
    response_dict['version'] = '1.0'
    response_dict['response'] = response_field_builder_with_reprompt_and_card(outputSpeech_text, card_text, card_title, reprompt_text, value)
    return response_dict





LINE_M8 = 'venmo'
LINE_B52 = 'lebron'

STOP_10_A = 'Peyton'
STOP_10_B = 'Julian'
STOP_10_GREENWICH = 'office'
STOP_GREEN_AVE_CLASSON_AVE = 'Abhi'

DIRECTION_WEST = 'west'
DIRECTION_EAST = 'east'

DATE_WEEKDAY = 'weekday'
DATE_SATURDAY = 'saturday'
DATE_SUNDAY = 'sunday'

BUS_SCHEDULE = {
    LINE_M8: {
        STOP_10_A: {
            DIRECTION_WEST: {
                DATE_SATURDAY: [
                    datetime.time(7, 33),
                    datetime.time(8, 3),
                    datetime.time(8, 33),
                    datetime.time(9, 3),
                    datetime.time(9, 33),
                    datetime.time(10, 3),
                    datetime.time(10, 33),
                    datetime.time(11, 3),
                    datetime.time(11, 33),
                    datetime.time(12, 3),
                    datetime.time(12, 33),
                    datetime.time(13, 3),
                    datetime.time(13, 33),
                    datetime.time(14, 3),
                    datetime.time(14, 33),
                    datetime.time(15, 3),
                    datetime.time(15, 33),
                    datetime.time(16, 3),
                    datetime.time(16, 33),
                    datetime.time(17, 3),
                    datetime.time(17, 33),
                    datetime.time(18, 3),
                    datetime.time(18, 33),
                    datetime.time(19, 3),
                    datetime.time(19, 33),
                    datetime.time(20, 3),
                    datetime.time(20, 33),
                    datetime.time(21, 3),
                    datetime.time(21, 33),
                    datetime.time(22, 3),
                    datetime.time(22, 33),
                    datetime.time(23, 3),
                    datetime.time(23, 33)
                ],
                DATE_SUNDAY: [
                    datetime.time(0,2),
                    datetime.time(0,32),
                    datetime.time(1,2),
                    datetime.time(7,32),
                    datetime.time(8,2),
                    datetime.time(8,32),
                    datetime.time(9,2),
                    datetime.time(9,32),
                    datetime.time(10,3),
                    datetime.time(10,33),
                    datetime.time(11,3),
                    datetime.time(11,33),
                    datetime.time(12,3),
                    datetime.time(12,33),
                    datetime.time(13,3),
                    datetime.time(13,33),
                    datetime.time(14,3),
                    datetime.time(14,33),
                    datetime.time(15,3),
                    datetime.time(15,33),
                    datetime.time(16,3),
                    datetime.time(16,33),
                    datetime.time(17,3),
                    datetime.time(17,33),
                    datetime.time(18,3),
                    datetime.time(18,33),
                    datetime.time(19,3),
                    datetime.time(19,32),
                    datetime.time(20,2),
                    datetime.time(20,32),
                    datetime.time(21,2),
                    datetime.time(21,32),
                    datetime.time(22,2),
                    datetime.time(22,32),
                    datetime.time(23,2),
                    datetime.time(23,32),
                ],
                DATE_WEEKDAY: [
                    datetime.time(0),
                    datetime.time(0,29),
                    datetime.time(1,2),
                    datetime.time(5,24),
                    datetime.time(5,54),
                    datetime.time(6,24),
                    datetime.time(6,49),
                    datetime.time(7,6),
                    datetime.time(7,21),
                    datetime.time(7,36),
                    datetime.time(7,51),
                    datetime.time(8,1),
                    datetime.time(8,11),
                    datetime.time(8,21),
                    datetime.time(8,31),
                    datetime.time(8,41),
                    datetime.time(8,51),
                    datetime.time(9,1),
                    datetime.time(9,16),
                    datetime.time(9,31),
                    datetime.time(9,50),
                    datetime.time(10,30),
                    datetime.time(10,50),
                    datetime.time(11,15),
                    datetime.time(11,40),
                    datetime.time(12,10),
                    datetime.time(12,40),
                    datetime.time(13,10),
                    datetime.time(13,40),
                    datetime.time(14,10),
                    datetime.time(14,40),
                    datetime.time(15),
                    datetime.time(15,20),
                    datetime.time(15,40),
                    datetime.time(16),
                    datetime.time(16,20),
                    datetime.time(16,40),
                    datetime.time(17),
                    datetime.time(17,20),
                    datetime.time(17,35),
                    datetime.time(17,50),
                    datetime.time(18),
                    datetime.time(18,20),
                    datetime.time(18,35),
                    datetime.time(18,50),
                    datetime.time(19,5),
                    datetime.time(19,20),
                    datetime.time(19,40),
                    datetime.time(20),
                    datetime.time(20,30),
                    datetime.time(21),
                    datetime.time(21,30),
                    datetime.time(22),
                    datetime.time(22,30),
                    datetime.time(23),
                    datetime.time(23,30)
                ]
            }
        },
        STOP_10_B: {
            DIRECTION_WEST: {
                DATE_WEEKDAY: [
                    datetime.time(0, 28),
                    datetime.time(1, 1),
                    datetime.time(5, 23),
                    datetime.time(5, 53),
                    datetime.time(6, 23),
                    datetime.time(6, 48),
                    datetime.time(7, 5),
                    datetime.time(7, 20),
                    datetime.time(7, 35),
                    datetime.time(7, 50),
                    datetime.time(8),
                    datetime.time(8, 10),
                    datetime.time(8, 20),
                    datetime.time(8, 30),
                    datetime.time(8, 40),
                    datetime.time(8, 50),
                    datetime.time(9),
                    datetime.time(9, 15),
                    datetime.time(9, 30),
                    datetime.time(9, 49),
                    datetime.time(10, 9),
                    datetime.time(10, 29),
                    datetime.time(10, 49),
                    datetime.time(11, 14),
                    datetime.time(11, 39),
                    datetime.time(12, 9),
                    datetime.time(12, 39),
                    datetime.time(13, 9),
                    datetime.time(13, 39),
                    datetime.time(14, 9),
                    datetime.time(14, 39),
                    datetime.time(14, 59),
                    datetime.time(15, 19),
                    datetime.time(15, 39),
                    datetime.time(15, 59),
                    datetime.time(16, 19),
                    datetime.time(16, 39),
                    datetime.time(16, 59),
                    datetime.time(17, 19),
                    datetime.time(17, 34),
                    datetime.time(17, 49),
                    datetime.time(18, 4),
                    datetime.time(18, 19),
                    datetime.time(18, 34),
                    datetime.time(18, 49),
                    datetime.time(19, 4),
                    datetime.time(19, 19),
                    datetime.time(19, 39),
                    datetime.time(19, 59),
                    datetime.time(20, 29),
                    datetime.time(20, 59),
                    datetime.time(21, 29),
                    datetime.time(21, 59),
                    datetime.time(22, 29),
                    datetime.time(22, 59),
                    datetime.time(23, 29),
                    datetime.time(23, 59)
                ]
            }
        },
        STOP_10_GREENWICH: {
            DIRECTION_EAST: {
                DATE_WEEKDAY: [
                    datetime.time(0, 1),
                    datetime.time(0, 36),
                    datetime.time(5, 1),
                    datetime.time(5, 31),
                    datetime.time(5, 56),
                    datetime.time(6, 21),
                    datetime.time(6, 41),
                    datetime.time(6, 54),
                    datetime.time(7, 4),
                    datetime.time(7, 14),
                    datetime.time(7, 24),
                    datetime.time(7, 34),
                    datetime.time(7, 44),
                    datetime.time(7, 54),
                    datetime.time(8, 4),
                    datetime.time(8, 14),
                    datetime.time(8, 24),
                    datetime.time(8, 36),
                    datetime.time(8, 51),
                    datetime.time(9, 11),
                    datetime.time(9, 31),
                    datetime.time(9, 51),
                    datetime.time(10, 11),
                    datetime.time(10, 31),
                    datetime.time(10, 56),
                    datetime.time(11, 21),
                    datetime.time(11, 51),
                    datetime.time(12, 21),
                    datetime.time(12, 51),
                    datetime.time(13, 21),
                    datetime.time(13, 51),
                    datetime.time(14, 21),
                    datetime.time(14, 41),
                    datetime.time(15, 1),
                    datetime.time(15, 21),
                    datetime.time(15, 41),
                    datetime.time(16, 1),
                    datetime.time(16, 21),
                    datetime.time(16, 41),
                    datetime.time(16, 56),
                    datetime.time(17, 11),
                    datetime.time(17, 26),
                    datetime.time(17, 41),
                    datetime.time(17, 56),
                    datetime.time(18, 11),
                    datetime.time(18, 26),
                    datetime.time(18, 46),
                    datetime.time(19, 6),
                    datetime.time(19, 26),
                    datetime.time(19, 56),
                    datetime.time(20, 26),
                    datetime.time(20, 56),
                    datetime.time(21, 26),
                    datetime.time(21, 56),
                    datetime.time(22, 26),
                    datetime.time(22, 56),
                    datetime.time(23, 26)
                ]
            }
        }
    },
    LINE_B52: {
        STOP_GREEN_AVE_CLASSON_AVE: {
            DIRECTION_EAST: {
                DATE_SUNDAY: [
                    datetime.time(4, 18),
                    datetime.time(5, 13),
                    datetime.time(5, 43),
                    datetime.time(6, 14),
                    datetime.time(6, 44),
                    datetime.time(7, 15),
                    datetime.time(7, 45),
                    datetime.time(8, 15),
                    datetime.time(8, 35),
                    datetime.time(8, 55),
                    datetime.time(9, 10),
                    datetime.time(9, 25),
                    datetime.time(9, 40),
                    datetime.time(9, 55),
                    datetime.time(10, 10),
                    datetime.time(10, 25),
                    datetime.time(10, 41),
                    datetime.time(10, 57),
                    datetime.time(11, 12),
                    datetime.time(11, 24),
                    datetime.time(11, 36),
                    datetime.time(11, 48),
                    datetime.time(12),
                    datetime.time(12, 13),
                    datetime.time(12, 25),
                    datetime.time(12, 37),
                    datetime.time(12, 49),
                    datetime.time(13, 1),
                    datetime.time(13, 13),
                    datetime.time(13, 25),
                    datetime.time(13, 37),
                    datetime.time(13, 49),
                    datetime.time(14, 1),
                    datetime.time(14, 13),
                    datetime.time(14, 25),
                    datetime.time(14, 37),
                    datetime.time(14, 49),
                    datetime.time(14, 59),
                    datetime.time(15, 09),
                    datetime.time(15, 20),
                    datetime.time(15, 30),
                    datetime.time(15, 40),
                    datetime.time(15, 50),
                    datetime.time(16),
                    datetime.time(16, 12),
                    datetime.time(16, 24),
                    datetime.time(16, 36),
                    datetime.time(16, 48),
                    datetime.time(17),
                    datetime.time(17, 12),
                    datetime.time(17, 24),
                    datetime.time(17, 36),
                    datetime.time(17, 48),
                    datetime.time(18),
                    datetime.time(18, 12),
                    datetime.time(18, 24),
                    datetime.time(18, 36),
                    datetime.time(18, 48),
                    datetime.time(18, 59),
                    datetime.time(19, 11),
                    datetime.time(19, 23),
                    datetime.time(19, 35),
                    datetime.time(19, 46),
                    datetime.time(19, 58),
                    datetime.time(20, 13),
                    datetime.time(20, 28),
                    datetime.time(20, 43),
                    datetime.time(20, 58),
                    datetime.time(21, 17),
                    datetime.time(21, 37),
                    datetime.time(21, 57),
                    datetime.time(22, 17),
                    datetime.time(22, 37),
                    datetime.time(22, 57),
                    datetime.time(23, 17),
                    datetime.time(23, 36),
                    datetime.time(23, 56)
                ]
            }
        }
    }

}
