import pyaudio
import requests
import base64

CHUNK = 8192  # Increase CHUNK size
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 8000
access_key = 'b4057c5f31eddb52b632163768055220'
access_secret = '5IZz8lHMXs7zNBJSdvW60P0iXXdARhko9fFwIbfB'

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

def recognize_song(audio_data):
    url = 'https://identify-ap-southeast-1.acrcloud.com/v1/identify'
    audio_base64 = base64.b64encode(audio_data).decode('utf-8')

    headers = {
        'Content-Type': 'application/octet-stream',
        'access-key': access_key,
        'signature': access_secret,
    }

    data = {
        'audio': audio_base64,
        'sample_bytes': len(audio_data),
        'sample_rate': RATE,
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        try:
            response_data = response.json()
        except ValueError as e:
            print(f"An error occurred during song recognition: Invalid response JSON format")
            print(f"Response Content: {response.content}")
            return None
        return response_data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during song recognition: {e}")
        return None

try:
    while True:
        try:
            data = stream.read(CHUNK)
            response = recognize_song(data)

            if response is not None:
                song_title = response.get('metadata', {}).get('music', [{}])[0].get('title')
                if song_title:
                    print(f"Song: {song_title}")
        except OSError as e:
            print(f"An error occurred during audio streaming: {e}")
            break
finally:
    if stream.is_active():
        stream.stop_stream()
    stream.close()
    audio.terminate()
