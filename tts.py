import malaya_speech
import numpy as np
from malaya_speech import Pipeline
import IPython.display as ipd

def response(string):
    male = malaya_speech.tts.fastspeech2(model = "osman")
    universal_melgan = malaya_speech.vocoder.melgan(model = 'universal-1024')

    responses = male.predict(string)
    # play audio
    y_ = universal_melgan(responses['universal-output'])
    return y_

string = "Helo, apa-apa yang saya boleh bantu"
# string = "Awak boleh melancong ke Kedah atau Pulau Penang"
ipd.Audio(response(string), rate=22050, autoplay=True)