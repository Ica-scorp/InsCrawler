import os
from claude_api import Client

def get_cookie():
    cookie = os.environ.get('__cf_bm=21dAVxlCxCWoh7nFoN__r6oTa9G.rXzOv6lWtlJa0dE-1694990139-0-AR/BqcPDadSYx7log9O7TIJhDWg6lnCgj64bQt51XXsxwyXCSTkcM4thQUuh1aW0ehKOpfEZ7dtcBCUND5FkPmQ=; cf_clearance=9HHNtwQLvP1CibWT1q_aqxG7c8.70UNZfTVXmv5Tlis-1694990139-0-1-b3484eab.219567a1.e449114b-0.2.1694990139; sessionKey=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; intercom-device-id-lupk8zyo=3354b9cd-ee05-4e51-92d2-77f1dfe68f56; intercom-session-lupk8zyo=Q2NCR2dEMjEyN3N6SVdKNC9yc1NXQ1VuRkJPZXVRdUx4YWc5ekVrSUFDazFKVXI4N1ZmajZkbHdBTG1Ic1ovMS0tU1krbkJvU0JmeXhkWUtZTzF5dHMxdz09--a195897b634de3d00cb0e15961ce8bee26bd4f93')
    if not cookie:
        raise ValueError("Please set the 'cookie' environment variable.")
    return cookie

def main():
    cookie = get_cookie()
    claude = Client(cookie)
    conversation_id = None

    print("Welcome to Claude AI Chat!")

    while True:
        user_input = input("You: ")

        if user_input.lower() == 'exit':
            print("Thank you!")
            break

        if not conversation_id:
            conversation = claude.create_new_chat()
            conversation_id = conversation['uuid']

        response = claude.send_message(user_input, conversation_id)
        print("Chatbot:", response)

if __name__ == "__main__":
    main()