import requests
import json
import base64
import pyaudio
import wave

def record_audio(file_path, duration=10):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=1024)

    print("Recording...")
    frames = []
    for i in range(0, int(44100 / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

    print("Recording complete.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(file_path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()

def recognize_music(file_path, host, access_key, secret_key):
    url = f"https://{host}/v1/identify"

    headers = {
        "Content-Type": "application/json",
        "access-key": access_key,
        "data-type": "audio",
        "signature-version": "1",
        "signature": "",  # Leave it empty for now
    }

    with open(file_path, "rb") as audio_file:
        audio_data = base64.b64encode(audio_file.read()).decode("utf-8")

    data = {
        "audio": {
            "data": audio_data
        },
        "recognize_type": 1,
        "filter": "music",
        "data_type": 0,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    print(response.json())


if __name__ == "__main__":
    host = "identify-ap-southeast-1.acrcloud.com"
    access_key = "c65802780a85c4012a3405e0e4504f5c"
    secret_key = "yEV2F2TzArnz6GvJ4T26oE5GUk0PRCWIgY3jtVW9"
    file_path = "sample.wav"

    record_audio(file_path)
    recognize_music(file_path, host, access_key, secret_key)
