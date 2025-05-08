from google import genai
import dotenv
import os
from stt import recognize_speech 
dotenv.load_dotenv()

client = genai.Client(api_key="")
model_name = "gemini-1.5-pro"


def clean_response(response_text):
    result = response_text
    result = result.replace("```json","")
    result = result.replace("```","")
    return result


def handle_errors_in_execution(user_prompt,image, context):

    base_prompt = """"""


def generate_normalized_steps(user_prompt,image):

    base_prompt = """You're a computer assistant that helps user to operate pc on the users behalf.
    Your task is to generate steps to achieve the goal given by the user.
    Now break down the task given below in steps that can be easily executed individually
    """ + user_prompt + """

    This is the prompt given by the user now you've to break it into easy steps.
    
    
    For ex. the user prompt could be
    
    user prompt : Open control panel and uninstall Brackets
    
    """





def generate_steps(user_prompt, memory, gui_status ,image):

    base_prompt = """
    You're a computer assistant that helps user to operate pc on the users behalf.
    Your task is to generate steps to achieve the goal given by the user.
    Only give single action every time.

    You can only perform four types of action which are.

    A) open_active_window
    b) keyboard_keys_click
    c) click_element
    d) input_text
    c) keyboard_input

    You've use these action depending on the situation, you'll be provided with current active window, all background active windows, current window all interactive elements name.
    You'll have to figure out how to use these actions to execute the task given and these buttons are everything you need.
    If you've to open control panel, you can simply use keyboard keys action for example click window key, focus will be on search bar so again enter keyboard_input to search control pannel,..... 


    This is the format you'll be returning the steps in the given format below.
    You'll return a list of actions like this where action object is given.
    Output must be strictly in json string format.
    Use this json schema
    In Intent tab explain the intent very explicitly.

    [action]

    {"Reason" : "Brief reason why we're performing this action.",
     "action" : "click_element(element_name)",
     "memory" : "Explain the whole status in brief, list down all the important things that needs to be knows for possible future use.",
     "taskstatus" : "Return if true or false, if true then task is completed for example if certain task no longer requires steps or already completed else false"}

     
    user query is : Open chrome and search for tom cruise and return his info.

    With this query you'll get a starting point which will be a screenshot of the current session in the desktop.
    Also you'll have information on all the current active windows and it's all interactive elements and background active windows.

    """+ gui_status + """   

    Your task will be to see what's going on and what steps should you take next to execute this task succesfully without 
    interfaring with other ongoing tasks.


    The sample output for this given task should be
    Assuming user is on desktop screen with no tasks going on and chrome is not available on desktop screen.
    Don't input any special characters or extra information unless needed. Keep it simple.

    []

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


def generate_steps_to_execute(user_prompt, image):

    base_prompt = r"""
    You're a computer assistant that helps user to break down steps for tasks in his computer.
    The example user query could be search for open calculator app and calculate 10 + 10.
    The response should be like this in json.

    ["Open Calculator Application" , "Perform 10 + 10 Calculation"]

    Second example

    Open VS Code and create new project. Create a python file write hello world program in it and run.

    The response should be like this in json

    ["Open VS Code", "Create New Project", "Create New Python File" , "Open New File And Write Hello World In Python", "Execute the file]

    I've attached a image as the current starting point. This is where the computer is right now.

    """

    response = client.models.generate_content(
    model=model_name,
    contents=[base_prompt, image],
    )
    
    return clean_response(response.text)