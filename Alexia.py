import openai
import pyttsx3
import speech_recognition as sr

openai.api_key = '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'

engine = pyttsx3.init()

voices = engine.getProperty('voices')
portuguese_voice = None
for voice in voices:
    if 'portuguese' in voice.languages:
        portuguese_voice = voice
        break
    if portuguese_voice is not None:
        engine.getProperty('voice', portuguese_voice.id)
    else:
        print('Não foi econtrada nenhuma voz em portugues')
        
        def trascrible_audio_to_text(filename):
            recognizer = sr.Recognizer()
            with sr.AudioFile(filename) as source:
                audio = recognizer.record(source)
            try:
                return recognizer.recognize_google_cloud(audio)
            except:
                print('Skipping unknown error')
                
def generate_response(prompt):
    response = openai.Completion.create(
        engine = 'text-davinci-003',
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response['choices'][0]['text']

def speak_text(text):
    engine.say(text)
    engine.runAndWait()
    
def main():
    while True:
        print('digite ´genius´ para começar a gravar sua pergunta')
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                trascription = recognizer.recognize_google_cloud(audio, language='pt-br')
                if trascription.lower() == 'genius':
                    
                    filename = 'input.wav'
                    print('Faça sua pergunta...')
                    with open(filename, 'wb') as f:
                        f.write(audio.get_wav_data())
                        
                        
                text = trascrible_audio_to_text(filename)
                if text:
                    print(f'vc disse {text}')
                    
                    response = generate_response(text)
                    print(f'GPT disse {response}')
                    
                    speak_text(response)
            except  Exception as e:
                print('Ocorreu um erro: {}'.format(e))

if __name__ == '__main__':
    main()                      
                                        