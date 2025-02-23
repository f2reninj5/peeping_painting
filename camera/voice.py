import queue
import sounddevice as sd
import vosk
import json

def voice():
    painting_words = ["painting", "paint", "george orwell", "george"]
    listen_words = ["listen"]

    global ignore_flag
    ignore_flag = False
    ignore_words = ["ignore", "ignoring"]

    global freeze_flag
    freeze_flag = False
    freeze_words = ["freeze", "stop", "halt"]
    unfreeze_words = ["restart", "start", "begin"]

    global iris_file
    iris_file = "iris.jpg"
    red_words = ["red", "read", "maroon"]
    blue_words = ["blue", "blew", "cyan"]
    green_words = ["green"]
    brown_words = ["brown"]


    model_path = "vosk-model-small-en-us-0.15"

    model = vosk.Model(model_path)

    audio_queue = queue.Queue()

    def audio_callback(indata, frames, time, status):
        audio_queue.put(bytes(indata))

    sample_rate = 16000

    devices = sd.query_devices()
    for i, device in enumerate(devices):
        if device['max_input_channels'] > 0:
            dindex = device['index']

    try:
        with sd.RawInputStream(device = dindex, channels = 1, samplerate = sample_rate, blocksize=8000, dtype='int16',
                            channels=1, callback=audio_callback):
            # print("Listening... Press Ctrl+C to stop.")
            recognizer = vosk.KaldiRecognizer(model, sample_rate)

            while True:
                data = audio_queue.get()

                if recognizer.AcceptWaveform(data):
                    result = recognizer.Result()
                    result_dict = json.loads(result)
                    rec_text = result_dict.get('text', '')
                    # print(f"Recognized Text: {rec_text}")

                    if any(word in rec_text for word in painting_words) or listening:
                        if any(word in rec_text for word in listen_words):
                            if listening == True:
                                listening = False
                            else:
                                listening = True
                        if any(word in rec_text for word in ignore_words):
                            # print(" -- IGNORE -- ")
                            if ignore_flag == False:
                                ignore_flag = True
                            else:
                                ignore_flag = False
                        if any(word in rec_text for word in freeze_words):
                            # print(" -- FREEZE -- ")
                            if freeze_flag == False:
                                freeze_flag = True
                            else:
                                freeze_flag = False
                        if any(word in rec_text for word in unfreeze_words):
                            # print(" -- UNFREEZE -- ")
                            freeze_flag = False
                        if any(word in rec_text for word in red_words):
                            # print(" -- RED EYES -- ")
                            iris_file = "red_iris.jpg"
                        if any(word in rec_text for word in blue_words):
                            # print(" -- BLUE EYES -- ")
                            iris_file = "blue_iris.jpg"
                        if any(word in rec_text for word in green_words):
                            # print(" -- GREEN EYES -- ")
                            iris_file = "iris.jpg"
                        if any(word in rec_text for word in brown_words):
                            # print(" -- BROWN EYES -- ")
                            iris_file = "brown_iris.jpg"

                # else:
                #     partial_result = recognizer.PartialResult()
                #     partial_result_dict = json.loads(partial_result)
                #     print(f"Partial Result: {partial_result_dict.get('partial', '')}")

    # except KeyboardInterrupt:
    #     print("\nTerminated by user")
    except Exception as e:
        print(f"An error occurred: {e}")

# voice()