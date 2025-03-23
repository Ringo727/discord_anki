from random import choice, randint

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == "":
        return "Quiet..."
    elif "hello" in lowered:
        return "Hello there!"
    elif "roll dice" in lowered:
        return f"You Rolled: {randint(1, 6)}"
    # else:
        # return choice(["I don't understand...", 
        #                 "What are you saying...?",
        #                 "Try that again..."])
    
    if "give card" in lowered:
        return "Here's your card!"
    
# def reaction_response() -> str:
    # return ""