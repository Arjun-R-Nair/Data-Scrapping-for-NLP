import nltk
import os
import csv
from nltk.sentiment import SentimentIntensityAnalyzer

def sentiment_analysis(text):
    sid = SentimentIntensityAnalyzer()
    
    # removing words from the text that are in the list of stop words
    words = [word.lower() for word in nltk.word_tokenize(text) if word.lower() not in stop_words]
    filtered_text = ' '.join(words)
    
    # returning all sentiment scores after calculations
    sentiment = sid.polarity_scores(filtered_text)
    return sentiment['pos'],sentiment['neg'],sentiment['compound']

text_folder = "D:\EDUCATION\OTHERS\MACHINE LEARNING\Sentiment-Analysis\sentimentanalysis\data"
stop_words_folder = "StopWords"
words_folder = "MasterDictionary"
stop_words = set()
positive_words = set()
negative_words = set()

for filename in os.listdir(stop_words_folder):
    with open(os.path.join(stop_words_folder, filename), 'r') as file:
        stop_words.update(file.read().split())

for filename in os.listdir(words_folder):
    if filename.endswith(".txt"):
        word_file = os.path.join(words_folder, filename)
        with open(word_file) as file:
            words = file.read().splitlines()
        if "positive-words" in filename:
            positive_words.update(words)
        elif "negative-words" in filename:
            negative_words.update(words)
results =[]
for filename in os.listdir(text_folder):
    text_file_path = os.path.join(text_folder, filename)
    if not os.path.exists(text_file_path):
        results.append([0,0,0])
        continue
    with open(os.path.join(text_folder, filename), 'r') as text_file:
        text = text_file.read()
        positive, negative, compound = sentiment_analysis(text)
        results.append([positive, negative, compound])

with open("Output.csv", 'r') as file:
    reader = csv.reader(file)
    header = next(reader)
    positive_index = header.index("POSITIVE SCORE")
    negative_index = header.index("NEGATIVE SCORE")
    polarity_index = header.index("POLARITY SCORE")
    print(positive_index,negative_index,polarity_index)
    data = [row for row in reader]

for row, result in zip(data, results):
    row[positive_index] = result[0]
    row[negative_index] = result[1]
    row[polarity_index] = result[2]
    
print(data)
with open("Output.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(data)