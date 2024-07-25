def get_bot_response(user_input):
    responses = {
        "hello": "Hi there! How can I help you today?",
        "what is a stock?": "A stock represents a share in the ownership of a company.",
        "how do I buy stocks?": "You can buy stocks through a brokerage account.",
        "default": "Sorry, I didn't understand that."
    }
    return responses.get(user_input.lower(), responses["default"])
