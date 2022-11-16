from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

RESPONSES = {
    "START": "Welcome to John and Kherissa's gender reveal! A stork flies over to you and hands you an invitation. You open it and read, \"Come find out our baby's gender (not Taylor) in this choose-your-own-adventure game!\" \n\nReply back CONTINUE or STOP",
    "CONTINUE": "Hurray! You will need to get to Clemson first. How do you want to travel?\n\nReply back TRAIN or PLANE",
    "STOP": "We're sad you don't want to find out the gender! If you change your mind...\n\nReply back START",
    "TRAIN": "You get on the train. What a ride! Too bad you picked the train going to the Big Rock Candy Mountain. It's an easy mistake to make, but you still aren't gonna get there on this locomotive...\n\nReply back GIVE UP, TIME MACHINE or RUN",
    "PLANE": "Your flight was delayed-are you taking Spirit? You are able to rebook on a different flight, wait or just take a train.\n\nReply back REBOOK, WAIT or TRAIN",
    "GIVE UP": "Giving up so soon? When you start to head back you see spot a time machine!\n\nReply back TIME MACHINE or FIND OUT GENDER",
    "TIME MACHINE": "You reach into your backpack and dig around. Underneath the Oreo's is a strange device with \"Do not use!\" written on it in sharpie. You use it and go back in time to your earliest memory: picking how to get to Clemson for this very important gender reveal!\n\nReply back TRAIN or PLANE",
    "WALK": "On your walk, you find you're headed to Arizona! And right when you try to reroute your friendly neighborhood cop picks you up for being suspicious looking and takes you for a cosy night in the community jail. No agency here.\n\nReply back JAIL",
    "RUN": "Woo, good thing you had a consistent exercise routine before this. Eventually even your endurance gives out though. Hitchhiking looks more and more ideal. You stick out your thumb and two cars pull up beside you, a pink one and a blue one. Which one do you take? Will you just keep walking?\n\nReply back PINK, BLUE or WALK",
    "PINK": "Ah the open road. And it would seem an open tire too, what with that hissing coming from the front wheel. There's no AAA in sight, but you can see that blue car coming up behind you. Should you fix the pink car's tire? Or hitch a ride? Or just walk?\n\nReply back FIX TIRE, BLUE or WALK",
    "BLUE": "The driver of the blue car seems nice, like Arnold Schwarzenegger. He also happens to be Arnold Schwarzeneggar, as far as you can tell from the accent and abundance of biceps. He narrates a long story about being ruler of some strange land with high fuel prices when suddenly you realize that you actually are low on fuel. He pulls into a gas station, but, having spent his money on protein powder, can't afford to pay. Do you buy the gas? Or hitch a ride with the pink car that's coming up behind you?\n\nReply back PAY, PINK or WALK",
    "FIX TIRE": "Nice job fixing the tire! You pulled off the flat, got out the spare, put the spare back in the trunk, and threw the old tire back on the car. Whew, that's a lot of lug nuts! You're back to driving when the tire explodes. You have to figure out a new way to travel now!\n\nReply back RENTAL or TIME MACHINE",
    "REBOOK": "You rebook your flight, on Frountier this time and hop on the first flight out! Unfortunately there was baby in the cockpit pressing buttons and the plane is forced to crash land in Kansas.\n\nReply back RENTAL, TRAIN or TIME MACHINE",
    "WAIT": "You desperately need something in your stomach while you wait and see a pink granola bar and a blue gatorade at a nearby shop. You decide to buy one.\n\nReply back SNACK or DRINK",
    "PAY": "You pay for gas and watch GSTV while Arnold goes in to get a drink. It's BOGO day at the Circle-K (yay!) so he brings you back one as well. Which one do you take?\n\nReply back MILKSHAKE or DIET COKE",
    "SNACK": "You start feeling really sick like you have food poisoning. You're wondering if you should stick it out at the aitport or just go home and call it a day.\n\nReply back STICK or GIVE UP",
    "DRINK": "You are now feeling satisfied and your pink plane arrives to take you to South Carolina! When you arrive, you head to Clemson.\n\nReply back UBER or BUS",
    "STICK": "What a reaction! At least getting sick passed the time, you recover quickly and are able to hop on your blue plane to South Carolina! When you arrive, you head to Clemson by a pink bus or a blue uber.\n\nReply back UBER or BUS",
    "MILKSHAKE": "The milkshake tastes amazing! That's normal, but what's not normal is how a wormhole spontaneously develops in the  milkshake cup, pulling you into a mixture of space and time. It's cool, but you still wish you could have finished that milkshake. The wormhole drops you off in the middle of Clemson University, where to survive you must quickly join a sports team!\n\nReply back FOOTBALL or GYMANSTICS",
    "UBER": "A nice blue uber man takes you to John and Kherissa's home for the gender reveal.\n\nReply back KNOCK or BREAK IN",
    "BUS": "The nice pink bus driver Shelly drops you off at Clemson University and you're somehow recruited to play a sport!\n\nReply back FOOTBALL or GYMANSTICS",
    "DIET COKE": "The Diet Coke tastes like coke except with zero calories. Arnold drives you to the airport, he's got to get back to Cali! \n\nReply back PLANE or TIME MACHINE",
    "RENTAL": "You found an awesome discount on a blue rental car but as you're driving you break down.\n\nReply back UBER or BUS",
    "FOOTBALL": "You choose football, but it's not like you're very good at it. But Coach Dabo see's something in you. He wants you to join his coaching staff. Whaddaya say? Do you want to be a benchwarmer the rest of your life?\n\nReply back COACH or BENCHWARMER",
    "GYMNASTICS": "Ooh, you think you're flexible do you? You try out gymnastics and almost immediately break your leg. Then your arm. Then every bone in your spine. Great, you're finished warming up! First meet is against the University of Miami... are you ready to go?\n\nReply back PLANE or QUIT",
    "COACH": "Coach Dabo thinks you're just the bees knees. He signs you to a $3 million contract and you buy a mansion on the lake. I guess you forgot about the gender reveal, huh?\n\nReply back TIME MACHINE",
    "BENCHWARMER": "So, you're a benchwarmer? Too bad it's pretty warm already in South Carolina. Who needs benchwarmers anyway? The coaches kick you off the team and you're left wandering your by yourself on the streets. You realize though you're not far from John and Kherissa's house! You run up to the door and...\n\nReply back KNOCK or WALK",
    "KNOCK": "Hello, hello! Welcome to our Gender Reveal! We'd love to hear your guess for our baby's gender!\n\nReply back BOY or GIRL",
    "BREAK IN": "The neighbor calls the police and you are sadly taken to jail.\n\nReply back JAIL or TIME MACHINE",
    "QUIT": "Everyone knows that quiters quit. How do you get to John and Kherissa's?\n\nReply back UBER or WALK",
    "BOY": "Wow! You guessed it! We are having another boy around March 31st and we couldn't be more excited! Thanks for playing!\n\nReply back START",
    "GIRL": "Well, you had a 50/50 shot. Try again!\n\nReply back BOY or GIRL",
    "JAIL": "You stay the night and meet a friendly inmate who is starting up a work group!\n\nReply back BREAK OUT, JOIN GROUP or TIME MACHINE",
    "BREAK OUT": "You got out! Choose where you want to run to.\n\nReply back TRAIN or PLANE",
    "JOIN GROUP": "This work group is actually a workout group to play sports. You have to choose a sport to play.\n\nReply back FOOTBALL or GYMNASTICS",
    "FIND OUT GENDER": "It's either a boy or a girl!\n\nReply back START"
}

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)
    check = body.upper().strip()

    # Start our TwiML response
    resp = MessagingResponse()

    # Check against dictionary
    if check in RESPONSES:
        resp.message(RESPONSES[check])
    elif check == 'test':
        resp.message('Test successful')
    else:
        resp.message("Invalid response, please try again or reply \'START\' to start over")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)