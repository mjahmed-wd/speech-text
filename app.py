from flask import Flask, request, jsonify
from whisper_jax import FlaxWhisperPipline
import jax.numpy as jnp

app = Flask(__name__)

# Initialize the Whisper pipeline
pipeline = FlaxWhisperPipline("openai/whisper-tiny", dtype=jnp.bfloat16, batch_size=16)

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    try:
        # Check if the request contains a JSON payload with the file name
        if 'file_name' not in request.json:
            return jsonify({'error': 'No file name provided'})

        file_name = request.json['file_name']

        # Check if the file is an MP3 file
        if file_name.endswith('.mp3'):
            # Perform transcription
            outputs = pipeline(file_name, task="transcribe", return_timestamps=True)
            chunks = outputs["chunks"]

            # Return the results
            return jsonify(chunks)

        else:
            return jsonify({'error': 'Invalid file format. Please provide an MP3 file'})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
