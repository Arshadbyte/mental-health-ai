
import speech_recognition as sr
import pyttsx3

def recognize_speech_from_mic():
    """
    Transcribes speech from microphone input.
    Returns:
        str: The transcribed text, or an error message.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        st.info("Say something!")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Speech recognition service error: {e}"

def text_to_speech(text):
    """
    Converts text to speech and plays it.
    Args:
        text (str): The text to convert to speech.
    """
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    # Example usage
    print("Testing speech recognition...")
    input_text = recognize_speech_from_mic()
    print(f"You said: {input_text}")

    if input_text != "Could not understand audio" and not input_text.startswith("Speech recognition service error"):
        print("Testing text to speech...")
        text_to_speech(f"You just said: {input_text}")



