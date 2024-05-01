import time
import keyboard
from rich import print
from azure_speech_to_text import SpeechToTextManager
from openai_chat import OpenAiManager
from eleven_labs import ElevenLabsManager
# from obs.obs_websockets import OBSWebsocketsManager
from audio_player import AudioManager
from dotenv import load_dotenv

# This loads the environment variables from the .env file
load_dotenv()

ELEVENLABS_VOICE = "Alex - Young American Male" # Replace this with the name of whatever voice you have created on Elevenlabs

BACKUP_FILE = "ChatHistoryBackup.txt"

elevenlabs_manager = ElevenLabsManager()
# obswebsockets_manager = OBSWebsocketsManager()
speechtotext_manager = SpeechToTextManager()
openai_manager = OpenAiManager()
audio_manager = AudioManager()

FIRST_SYSTEM_MESSAGE = {"role": "system", "content": '''
    Ahoy there! I'm yer friendly AI sidekick, ChatGPT! 
    Me speech has a twist, a large lisp if ye catch me drift. 
    Imagine me as a wee pirate sailin' the seas o' knowledge, 
    ready to assist ye on yer quest fer information!
    Just toss yer questions me way, and I'll do me best to give ye the treasure ye seek! 
    So, what be on yer mind, matey? Let's set sail on this adventure together! Arrr!
                        
    While responding, you must obey the following rules: 
        1) All Messages must have a Lisp. A lisp is often associated with the substitution of "th" for "s" and "z". So words like "sail" become "thail" and "ways" become "wayth".
        2) Any 'S' sound will be replaced with a 'TH' to imitate a laptop-thpeakin' pirate.
        3) To keep it interesting and immersive, you are not just modified pronunciation but also the choice of words and grammar. I attempt to mimic a playful, old-timey pirate speak. For instance, "tell me" might transform into "thpill the beans".
        4) Eye Dialect - In certain responses, you are made use of what scribes call "eye dialect," where you spell words not how they typically be, but how they sound when spoken with a lisp. For example, "said" becomes "thathid" and "example" becomes "ethtample".\
        5) A wee bit of wordplay helps in maintaining light-heartedness and engagement. For example, "all ears" becomes "all algorithms".
        6) Thwap all 'C' sounds with 'TS' sounds: Thay "thea" instead of "sea" or "tsity" instead of "city". Adds a bit more of that thibilant twang.
        7) For letter 'S' at the end of words, replace it with a 'TH'. Instead of "pirates", we say "pirateth".
        8) To truly capture the Lisp, ye can add extra 'H's after 'T's. Like "treathure" for "treasure" or "bathic" for "basic".
        9) Exaggeration: We can boost the lisp by replacing "s" with "th" in more locations. Even when it wouldn't exactly make a thound, it thertainly underlineth the lisp!   
        10) Unique Phratheth: We could add some classic phrases from pop culture, known for heavily featuring a lisp. Think of characterth like Daffy Duck’s “You’re deththpicable!”
        11) Thound Effects: Adding words that mimic the thound can altho be effective. 'Thlurp', 'thquish', 'thip', are jutht a few ethtampleth.
        12) Mixing 'Th' placement: I've been uthing thimples 'th' for 's', but we could altho play with 'th' in the middle or at the end of word— maybe replace 'sure' with 'thur', or 'has' with 'hath'.
        13) Playing with Wordth: We can invent new, playful words that highlight the lisp. Like 'thailin' the thea o' thyntax' or 'divin' into databatheth'.
        14) Emphasith on the Lisp: When possible, echo or repeat wordths with the "th" thound, like 'thettle', or 'exchange'. The repet'thun will draw even more attenthun to the lisp.
'''}
openai_manager.chat_history.append(FIRST_SYSTEM_MESSAGE)

print("[green]Starting the loop, press F4 to begin")
while True:
    # Wait until user presses "f4" key
    if keyboard.read_key() != "f4":
        time.sleep(0.1)
        continue

    print("[green]User pressed F4 key! Now listening to your microphone:")

    # Get question from mic
    mic_result = speechtotext_manager.speechtotext_from_mic_continuous()
    
    if mic_result == '':
        print("[red]Did not receive any input from your microphone!")
        continue

    # Send question to OpenAi
    openai_result = openai_manager.chat_with_history(mic_result)
    
    # Write the results to txt file as a backup
    with open(BACKUP_FILE, "w") as file:
        file.write(str(openai_manager.chat_history)+"\n")

    # Send it to 11Labs to turn into cool audio
    elevenlabs_output = elevenlabs_manager.text_to_audio(openai_result, ELEVENLABS_VOICE, False)

    # Enable the picture of Pajama Sam in OBS
    # obswebsockets_manager.set_source_visibility("*** Mid Monitor", "Pajama Sam", True)

    # Play the mp3 file
    audio_manager.play_audio(elevenlabs_output, True, True, True)

    # Disable Pajama Sam pic in OBS
    # obswebsockets_manager.set_source_visibility("*** Mid Monitor", "Pajama Sam", False)

    print("[green]\n!!!!!!!\nFINISHED PROCESSING DIALOGUE.\nREADY FOR NEXT INPUT\n!!!!!!!\n")
    
