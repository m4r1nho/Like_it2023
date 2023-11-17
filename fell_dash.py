from google.cloud import language_v2
import pandas as pd
import threading
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import matplotlib
matplotlib.use('Agg')

#--------------------------------------------------------------------------------------------#
def sample_analyze_sentiment(text_content):

    client = language_v2.LanguageServiceClient()

    # Available types: PLAIN_TEXT, HTML
    document_type_in_plain_text = language_v2.Document.Type.PLAIN_TEXT

    # Set the language code to Portuguese for sentiment analysis
    language_code = "pt"  # Portuguese
    document = {
        "content": text_content,
        "type_": document_type_in_plain_text,
        "language_code": language_code,
    }

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v2.EncodingType.UTF32

    response = client.analyze_sentiment(
        request={"document": document, "encoding_type": encoding_type}
    )
    # Get the overall sentiment of the input document
    
    score = round(response.document_sentiment.score, 4)   
    #magnitude = round(response.document_sentiment.magnitude, 4)
    
    if __name__ == "__main__":
        print(f"Document sentiment score: {score}")
        #print(f"Document sentiment magnitude: {magnitude}")
        print(f"Language of the text: {response.language_code}")
        print(f"Sentence text: {text_content}")

    return score

def analyze_google(comments, num_threads=4):
    column_google = []
    # Divide the list of comments into chunks for parallel processing
    chunk_size = len(comments) // num_threads
    comment_chunks = [comments[i:i + chunk_size] for i in range(0, len(comments), chunk_size)]

    # Create a list to store threads
    threads = []

    # Define a function to analyze the sentiment of a chunk of comments
    def analyze_chunk(chunk):
        for comment in chunk:
            if comment != '':
                analysis = sample_analyze_sentiment(comment)
                column_google.append(analysis)
                #column_google['Magnitude'].append(analysis[1])

    # Create and start threads
    for chunk in comment_chunks:
        thread = threading.Thread(target=analyze_chunk, args=(chunk,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    return column_google


#--------------------------------------------------------------------------------------------#
# a csv with comments and scores
def to_create(comments, analyze):
    
    # to remove null values
    for i in comments:
        if i == '' or i == None:
            comments.remove(i)

    df = pd.DataFrame({'Comentario': comments, 'Score': analyze}) # create a data frame

    df.to_csv('file_google.csv', index=False) # save to csv


#--------------------------------------------------------------------------------------------#


def create_cloud(comments, del_words):

    text = ' '.join(comments) # one string of all comments

    text.lower() # all letters are lowercase

    # remove stop words
    stop_words = set(stopwords.words('portuguese'))  # portuguese stop words
    
    del_words.extend(stop_words)

    words = nltk.word_tokenize(text) # tokenize 

    # filter
    filtered_words = [word for word in words if word not in del_words and len(word) > 1]
    filtered_text = ' '.join(filtered_words)

    # Crie um objeto WordCloud
    word_cloud = WordCloud(width=1600, height=700, background_color='azure', colormap='Dark2', 
                                  contour_color='black').generate(filtered_text)

    # show the WordCloud using matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig("cloud.png", bbox_inches='tight', pad_inches=0)
    plt.close()

#--------------------------------------------------------------------------------------------#


 

    