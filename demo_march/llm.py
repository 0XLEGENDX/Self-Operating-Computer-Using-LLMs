from google import genai
import dotenv
import os
from stt import recognize_speech 
dotenv.load_dotenv()

client = genai.Client(api_key="AIzaSyBbscjvZixMhAFIiF5IL3HWnKT-ZBE0-2s" )
model_name = "gemini-1.5-pro"


def clean_response(response_text):

    result = response_text
    result = result.replace("```json","")
    result = result.replace("```","")

    return result



def generate_steps(user_prompt, image):

    base_prompt = """
    You're a computer assistant that helps user to operate pc on the users behalf.
    Your task is to generate steps to achieve the goal given by the user.
    
    You can only perform two types of action which are mouse and keyboard.
    
    This is the format you'll be returning the steps in the given format below.
    You'll return a list of actions like this where action object is given.
    Output must be strictly in json string format.
    Use this json schema
    In Intent tab explain the intent very explicitly.

    [action,action]

    action = {
        intent: "Explain the task."
        inputType : mouse,keyboard
        actionType : move, left_click, right_click, doubleclick, scroll, type, press_key, press_key_combination
        key : ["CTRL" , "DELETE"]
        string_to_write : "string"
        location : [x,y] coordinates where to click or type.  Always return (-1 -1) because this feature is not available   
    }


    You'll have to breakdown the process into very small steps like move mouse, left click,etc.
    For example

    user query is : Open chrome and search for tom cruise and return his info.

    With this query you'll get a starting point which will be a screenshot of the current session in the desktop.

    Your task will be to see what's going on and what steps should you take next to execute this task succesfully without 
    interfaring with other ongoing tasks.


    The sample output for this given task should be
    Assuming user is on desktop screen with no tasks going on and chrome is not available on desktop screen.
    Don't input any special characters or extra information unless needed. Keep it simple.
    

    [{
    "intent" : "Click windows button to open the start menu",
    "inputType" : "keyboard",
    "actionType" : "press_key",
    "key" : ["WIN"],
    "location" : [-1,-1]
    },

    {
    "intent" : "Type chrome in the search bar",
    "inputType" : "keyboard",
    "actionType" : "type",
    "key" : [],
    "string_to_write" : "chrome",
    "location" : [-1,-1]
    },

    {
    "intent" : "Press enter to open chrome",
    "inputType" : "keyboard",
    "actionType" : "press_key",
    "key" : ["ENTER"],
    "location" : [-1,-1]
    },

    ......
    
    ]

    This is half example for the given task.


    user query for the task you've to return steps is : 
    """ + user_prompt +""" 
    
    Return the steps strictly in given format and pattern."""


    response = client.models.generate_content(
    model=model_name,
    contents=[base_prompt, image],
    )

    f = open("temp.txt","w")
    f.write(response.text)
    f.close()
    return clean_response(response.text)


def validate_action_step(action_step, image):

    intent = action_step

    base_prompt = f"""
    You're a computer assistant that helps user to verify if certain task is successfully completed on the computer.
    The task user wanted to perform was {intent} and I've attached image. Verify if the task is successfully completed or if there is any error or challenge.
    Strictly verify if all the things in the screenshot are correct or not.
    For example
    1) Check if window opened is correct.
    2) Check if screenshot is truly the end of the task.
    3) Check if data inputs and outputs are exactly what they should be.
    
    Return format should be in the given format and strictly in json string format.

    You're a task verifier that will check if the given task is completed or not.
    The task is {intent}. Check if the given condition is the task is satisfied in the given image.
    
    """ + """
    {"status" : true or false,
     "reason" : tell if completed or not and if not why}
    """

    response = client.models.generate_content(
    model=model_name,
    contents=[base_prompt, image],
    )
    
    return clean_response(response.text) 
 