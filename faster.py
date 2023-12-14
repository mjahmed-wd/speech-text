from faster_whisper import WhisperModel
import json
from faster_whisper import WhisperModel
import json

model_size_or_path = "base"
fileName = 'ai_video_editor_sample_cropped_file.flac'

model = WhisperModel(model_size_or_path, device="auto", cpu_threads=4)

segments, _ = model.transcribe(fileName,beam_size=1, word_timestamps=True)

segment_list = []
for segment in segments:
    word_list = []
    for word in segment.words:
        word_dict = {
            "confidence": word.probability,
            "startTime": word.start,
            "endTime": word.end,
            "word": word.word
        }
        word_list.append(word_dict)
    segment_dict = {
        "words": word_list
    }
    segment_list.append(segment_dict)

print(segment_list)
