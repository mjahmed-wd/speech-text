# Transcribe Python

This is a Python application built with FastAPI for transcribing audio files.

## Getting Started

To get started with this project, follow the steps below:

### Usage

1. Start the FastAPI server:

    ```
    docker compose up
    ```

2. Open your web browser and go to `http://localhost:8000` to access the API.

3. Use the following endpoints:

    - `GET /`: Returns a welcome message.
    - `POST /transcribe`: Transcribes an audio file. Send a JSON payload with the `fileUrl` parameter containing the URL of the audio file.
```
{"fileUrl": "https://raw.githubusercontent.com/mjahmed-wd/speech-text/main/files/audio.mp3"}
```

### Acknowledgements

- [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper) - Faster Whisper transcription with CTranslate2


### Large-v2 model on GPU

| Implementation | Precision | Beam size | Time | Max. GPU memory | Max. CPU memory |
| --- | --- | --- | --- | --- | --- |
| openai/whisper | fp16 | 5 | 4m30s | 11325MB | 9439MB |
| faster-whisper | fp16 | 5 | 54s | 4755MB | 3244MB |
| faster-whisper | int8 | 5 | 59s | 3091MB | 3117MB |

*Executed with CUDA 11.7.1 on a NVIDIA Tesla V100S.*

### Small model on CPU

| Implementation | Precision | Beam size | Time | Max. memory |
| --- | --- | --- | --- | --- |
| openai/whisper | fp32 | 5 | 10m31s | 3101MB |
| whisper.cpp | fp32 | 5 | 17m42s | 1581MB |
| whisper.cpp | fp16 | 5 | 12m39s | 873MB |
| faster-whisper | fp32 | 5 | 2m44s | 1675MB |
| faster-whisper | int8 | 5 | 2m04s | 995MB |

*Executed with 8 threads on a Intel(R) Xeon(R) Gold 6226R.*
