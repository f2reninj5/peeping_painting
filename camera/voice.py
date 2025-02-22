def voice():
    import queue
    import sounddevice as sd
    import vosk
    import sys
    import json

    global ignore_flag
    ignore_flag = False
    ignore_words = ["ignore", "ignoring"]

    global freeze_flag
    freeze_flag = False
    freeze_words = ["freeze", "stop", "halt"]
    unfreeze_words = ["restart", "start", "begin"]


    model_path = "vosk-model-small-en-us-0.15"

    model = vosk.Model(model_path)

    audio_queue = queue.Queue()

    def audio_callback(indata, frames, time, status):
        if status:
            print(f"Error: {status}", file=sys.stderr)
        audio_queue.put(bytes(indata))

    sample_rate = 16000

    try:
        with sd.RawInputStream(samplerate=sample_rate, blocksize=8000, dtype='int16',
                            channels=1, callback=audio_callback):
            print("Listening... Press Ctrl+C to stop.")
            recognizer = vosk.KaldiRecognizer(model, sample_rate)

            while True:
                data = audio_queue.get()

                if recognizer.AcceptWaveform(data):
                    result = recognizer.Result()
                    result_dict = json.loads(result)
                    rec_text = result_dict.get('text', '')
                    print(f"Recognized Text: {rec_text}")

                    if "painting" in rec_text:
                        if any(word in rec_text for word in ignore_words):
                            print(" -- IGNORE -- ")
                            if ignore_flag == False:
                                ignore_flag = True
                            else:
                                ignore_flag = False
                        if any(word in rec_text for word in freeze_words):
                            print(" -- FREEZE -- ")
                            if freeze_flag == False:
                                freeze_flag = True
                            else:
                                freeze_flag = False
                        if any(word in rec_text for word in unfreeze_words):
                            print(" -- UNFREEZE -- ")
                            freeze_flag = False

                else:
                    partial_result = recognizer.PartialResult()
                    partial_result_dict = json.loads(partial_result)
                    print(f"Partial Result: {partial_result_dict.get('partial', '')}")

    except KeyboardInterrupt:
        print("\nTerminated by user")
    except Exception as e:
        print(f"An error occurred: {e}")

voice()