import os

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import requests
from os import path
from pydub import AudioSegment
from scipy.io import wavfile


def extract_name_from_url(url):
    return url.split('/')[-1].split('.mp3')[0]


def get_urls(url_filename):
    url_list_file = open(url_filename, 'r')
    urls = url_list_file.read().split('\n')
    url_list_file.close()
    return set(urls)


def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        language_code='en-NZ')

    operation = client.long_running_recognize(config, audio)

    print(extract_name_from_url(gsc))
    response = operation.result(timeout=90)

    return response.results[0].alternatives[0].transcript


def download_file_to(url, file_path):
    audio_file = requests.get(url)
    open(file_path, 'wb').write(audio_file.content)


def convert_mp3_to_wav(audio_file_path):
    src = os.path.join(os.getcwd(), audio_file_path)
    dst = os.path.join(os.getcwd(), os.path.splitext(audio_file_path)[0] + '.wav')

    print(src)
    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")
    return dst


def make_wav_file_mono(wav_file_path):
    src = wav_file_path
    dst = os.path.splitext(wav_file_path)[0] + 'mono.wav'

    rate, data = wavfile.read(path)
    # data0 is the data from channel 0.
    data0 = data[:, 0]

    return dst


def transcribe_url_list(url_list):
    for url in url_list:
        filename = extract_name_from_url(url)
        mp3_file_path = 'temp_files\\' + filename + '.mp3'
        print("Downloading {}...".format(filename))
        # download_file_to(url, mp3_file_path)
        print("Converting to wav...")
        wav_file_path = convert_mp3_to_wav(mp3_file_path)
        print("Converting to mono...")
        mono_wav_file_path = make_wav_file_mono(wav_file_path)


def main():
    url_list = get_urls('url_list.txt')
    transcribe_url_list(url_list)
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\\Users\\ollie\\Dropbox\\Other\\My Project-a695b922503a.json'
    transcript = transcribe_gcs("gs://podcastfiles/clintsongmono.wav")
    print(transcript)


if __name__ == '__main__':
    main()
