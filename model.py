from faster_whisper import WhisperModel

model_size_or_path = "base"

model = WhisperModel(model_size_or_path, device="auto", cpu_threads=4)

def transcribe_file(fileName):
    print('Started transcribing file: ' + fileName)
    
    segments, _ = model.transcribe(fileName, beam_size=1, word_timestamps=True)

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

    print('Finished transcribing file: ' + fileName)

    return segment_list