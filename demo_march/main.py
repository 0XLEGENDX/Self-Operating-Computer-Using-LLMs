import llm
import voice
import screenshot
import keyboard
import json
import time
from stt import recognize_speech 

speech_enabled = False

while(True):

    if(speech_enabled):
        print("Listening......")
        query = recognize_speech()
        if query: 
            prompt = query
        else:
            print("No valid input detected.")
            continue
        
    else:
        voice.text_to_speech("Enter your task : .")
        prompt = input("Enter your task : ")

    session_screenshot = screenshot.take_screenshot()
    action_steps = llm.generate_steps(prompt,session_screenshot)
    action_steps = json.loads(action_steps)
    for action in action_steps:
        print(action)
        task = action["intent"]
        voice.text_to_speech(task)
        keyboard.add_hotkey("ctrl+shift+a", screenshot.take_screenshot)
        keyboard.wait("Esc")
        session_screenshot = screenshot.fetch_screenshot()
        action_result = json.loads(llm.validate_action_step(task , session_screenshot))
        print(action_result)
        if(action_result["status"]):
            voice.text_to_speech(action_result["reason"])
        else:
            voice.text_to_speech("Something Went Wrong!")
            break
    
    voice.text_to_speech(prompt + " Executed Successfully.")
        # time.sleep(100)





