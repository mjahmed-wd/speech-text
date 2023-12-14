from faster_whisper import WhisperModel

model_size_or_path = "tiny"

model = WhisperModel(model_size_or_path, device="auto", compute_type='int8', cpu_threads=4, )

def transcribe_file(fileUrl):
    print('Started transcribing file: ' + fileUrl)
    
    segments, _ = model.transcribe(fileUrl, beam_size=5, word_timestamps=True)

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

    print('Finished transcribing file: ' + fileUrl)

    return segment_list