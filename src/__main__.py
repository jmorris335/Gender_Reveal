from src.messaging import Messages

def main():
    messages = Messages()
    messages.sendMessage(body='Hi Grandma, just reply START to this message!', to_num='+19189319751')