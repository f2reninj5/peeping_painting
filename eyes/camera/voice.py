def voice():
    import queue
    import sounddevice as sd
    import vosk
    import sys
    import json

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
                    print(f"Recognized Text: {result_dict.get('text', '')}")
                else:
                    partial_result = recognizer.PartialResult()
                    partial_result_dict = json.loads(partial_result)
                    print(f"Partial Result: {partial_result_dict.get('partial', '')}")

    except KeyboardInterrupt:
        print("\nTerminated by user")
    except Exception as e:
        print(f"An error occurred: {e}")

voice()