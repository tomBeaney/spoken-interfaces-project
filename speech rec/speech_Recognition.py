import speech_recognition as sr
import requests
import matplotlib.pyplot as plt
import numpy as np

# Local server URL where Unity will listen for the text
server_url = 'http://localhost:5000/receive_text'

# Initialize the recognizer
recognizer = sr.Recognizer()

# Use the selected microphone as the audio source, here microphone 1 is my advanced microphone
with sr.Microphone(1) as source:
    print("Listening...")

    # Adjust for ambient noise for better recognition
    recognizer.adjust_for_ambient_noise(source)
    # Continuous listening loop
    while True:
        try:
            # Capture the audio from the microphone
            audio_data = recognizer.record(source, duration=7)  # Record audio from the microphone for 7 seconds change as needed
            audio_samples = np.frombuffer(audio_data.frame_data, dtype=np.int16)

            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio_data)
            time = np.arange(0, len(audio_samples)) / audio_data.sample_rate
            #confidence value return
            confidence = recognizer.recognize_google(audio_data,show_all=True)
            #print(confidence)
            #make the payload for the server and send it
            payload = {'text': text}
            response = requests.post(server_url, json=payload)
            if response.status_code == 200:
                print("Text sent to the server successfully")
            else:
                print("Failed to send text to the server")

            # Print the recognized speech
            print("You said:", confidence['alternative'][0]['transcript'], ',with Confidence: ',
                  confidence['alternative'][0]['confidence'])
            # prints out the said line recognised with a confidence value
            print('Alternatives for the spoken phrase: ', end='')
            for i in range(0, len(confidence['alternative'])):
                if i != 0:
                    print(confidence['alternative'][i]['transcript'], end=', ')
            # prints out all of the alternatives that might be in the recongised audio
            print('')
            #display the captured audio as a wave form
            plt.figure(figsize=(10, 4))
            plt.plot(time, audio_samples, linewidth=0.5)
            plt.xlabel('Time (s)')
            plt.ylabel('Amplitude')
            plt.title('Audio Waveform')
            plt.show() #show the captured waveform
        except sr.UnknownValueError: #if nothing is detected then send back ... to show nothing is detected
            # make the payload for the server and send it
            payload = {'text': str(...)}
            response = requests.post(server_url, json=payload)
            if response.status_code == 200:
                print("Text sent to the server successfully")
            else:
                print("Failed to send text to the server")
            print("Could not understand the audio")

        except sr.RequestError as e: #if not connected to internet
            print("Error fetching results; {0}".format(e))

        except KeyboardInterrupt: #stops the program
            print("Stopping the program")
            break