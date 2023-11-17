from transformers import pipeline # to get model
from googletrans import Translator # to get the translator
import threading
import pandas as pd

# the classifier works with phrases in English, so it is necessary to translate 
# them as our focus is research in Portuguese
classifier = pipeline("text-classification", model='bhadresh-savani/distilbert-base-uncased-emotion')

# function that translates a sentence in Portuguese into English
def translate(sentence):
    translator = Translator()
    translation = translator.translate(sentence, src='pt', dest='en')

    return translation.text


def hf_analysis_english(comment):
  prediction = classifier(comment) # classifier, it creates a list
  prediction = prediction[0] # select the first, now it's a dict
  prediction = prediction['label'] # select the label, now it's an emotion
  return prediction


# function to count
# if you don't have the emotion in the list, it's because there are 0
def count_list(list_emotions):
    
    if 'love' not in list_emotions:
        love = 0
    else:
        love = list_emotions.count('love')

    if 'joy' not in list_emotions:
        joy = 0
    else:
        joy = list_emotions.count('joy') 

    if 'surprise' not in list_emotions:
        surprise = 0
    else:
        surprise = list_emotions.count('surprise')

    if 'fear' not in list_emotions:
        fear = 0
    else:
        fear = list_emotions.count('fear') 

    if 'anger' not in list_emotions:
        anger = 0
    else:
        anger = list_emotions.count('anger') 

    if 'sadness' not in list_emotions:
        sadness = 0
    else:
        sadness = list_emotions.count('sadness')
    
    values = [love, joy, surprise, fear, anger, sadness]   
    return values

                          
def hf_analysis(comments, language):
    list_emotions = []
    threads = []

    # Function to sentiment analysis on a single comment
    def process_comment(comment):
        if language == 'pt': # if the sentence is in Portuguese, it needs an English translation

            english_sentence = translate(comment)

        elif language == 'en':# no translation
            english_sentence = comment

        emotion = hf_analysis_english(english_sentence)
        list_emotions.append(emotion)

    # Create threads to process each comment
    for comment in comments:
        thread = threading.Thread(target=process_comment, args=(comment,))
        threads.append(thread)
        thread.start()

    # wait for all threads to finish
    for thread in threads:
        thread.join()

    # if the function is used with sentences already in English, then I need the list of emotions,
    # if I needed to translate I can count the number of emotions

    if language == 'pt':
        r_csv(list_emotions)

        return count_list(list_emotions)
    
    if language == 'en':
        return list_emotions

# rewrite the csv file, putting an emotion column
def r_csv(list_emotions):
    
    file = 'file_google.csv'
    df = pd.read_csv(file)

    df['Emotion'] = list_emotions
    df.to_csv(file, index=False)


