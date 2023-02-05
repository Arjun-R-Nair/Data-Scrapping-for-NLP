import csv
import os
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

def sentiment_analysis(text):
    sid = SentimentIntensityAnalyzer()
    #removing stop words from the text
    words = [word.lower() for word in nltk.word_tokenize(text) if word.lower() not in stop_words]
    filtered_text = ' '.join(words)
    sentiment = sid.polarity_scores(filtered_text)
    return sentiment['pos'],sentiment['neg'],sentiment['compound']

def calculate_metrics(text):
    blob = TextBlob(text)
    subject = blob.sentiment.subjectivity
    if len(blob.sentences) > 0:
        avg_sentence_length = sum([len(sentence.words) for sentence in blob.sentences]) / len(blob.sentences)
        avg_number_of_words_per_sentence = len(blob.words) / len(blob.sentences)
    else:
        avg_sentence_length = 0
        avg_number_of_words_per_sentence = 0
    complex_word_count = sum([1 for word in blob.words if syllable_count(word) >= 3])
    if  len(blob.words) > 0:
        percentage_of_complex_words = complex_word_count / len(blob.words) * 100
        avg_word_length = sum([len(word) for word in blob.words]) / len(blob.words)
    else:
        percentage_of_complex_words = 0
        avg_word_length = 0
    fog_index = 0.4 * ((avg_sentence_length + percentage_of_complex_words) / 2)
    total_syllables = 0
    for word in blob.words:
        total_syllables += syllable_count(word)
    if len(blob.words) > 0:
        average_syllables_per_word = total_syllables / len(blob.words)
    else:
        average_syllables_per_word = 0
    personal_pronouns = ['I', 'me', 'my', 'mine', 'you', 'your', 'yours', 'he', 'him', 'his', 'she', 'her', 'hers', 'we', 'us', 'our', 'ours', 'they', 'them', 'their', 'theirs']
    personal_pronoun_count = sum([1 for word in blob.words if word.lower() in personal_pronouns])
    return subject, avg_sentence_length, percentage_of_complex_words, fog_index, avg_number_of_words_per_sentence, complex_word_count, len(blob.words),average_syllables_per_word, personal_pronoun_count, avg_word_length

def syllable_count(word):
    # function to get syllable count of a word
    vowels = "aeiouy"
    count = 0
    word = word.lower()
    if word[0] in vowels:
        count +=1
    for index in range(1,len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            count +=1
    if word.endswith("e"):
        count -= 1
    if word.endswith("le"):
        count+=1
    if count == 0:
        count +=1
    return count

text_folder = "D:\EDUCATION\OTHERS\MACHINE LEARNING\Sentiment-Analysis\sentimentanalysis\data"
stop_words_folder = "StopWords"
words_folder = "MasterDictionary"
stop_words = set()
positive_words = set()
negative_words = set()
results =[]

for filename in os.listdir(stop_words_folder):
    with open(os.path.join(stop_words_folder, filename), 'r') as file:
        stop_words.update(file.read().split())

for filename in os.listdir(words_folder):
    #adding all given postitive and negative words 
    if filename.endswith(".txt"):
        word_file = os.path.join(words_folder, filename)
        with open(word_file) as file:
            words = file.read().splitlines()
        if "positive-words" in filename:
            positive_words.update(words)
        elif "negative-words" in filename:
            negative_words.update(words)

for filename in os.listdir(text_folder):
    text_file_path = os.path.join(text_folder, filename)
    if not os.path.exists(text_file_path):
        results.append([0,0,0])
        continue
    with open(os.path.join(text_folder, filename), 'r') as text_file:
        text = text_file.read()
        positive, negative, compound = sentiment_analysis(text) 
        subject, avg_sentence_length, percentage_of_complex_words, fog_index, avg_number_of_words_per_sentence, complex_word_count, word_count, syllable_per_word, personal_pronoun_count, avg_word_length = calculate_metrics(text)
        results.append([positive, negative, compound, subject, avg_sentence_length, percentage_of_complex_words, fog_index, avg_number_of_words_per_sentence, complex_word_count, word_count, syllable_per_word, personal_pronoun_count, avg_word_length])

with open("Output.csv", 'r') as file:
    reader = csv.reader(file)
    header = next(reader)
    positive_index = header.index("POSITIVE SCORE")
    negative_index = header.index("NEGATIVE SCORE")
    polarity_index = header.index("POLARITY SCORE")
    subjectivity_index = header.index("SUBJECTIVITY SCORE")
    avg_sent_len_index = header.index("AVG SENTENCE LENGTH")
    per_cmplxwrds_index = header.index("PERCENTAGE OF COMPLEX WORDS")
    fog_ind_index = header.index("FOG INDEX")
    avg_nowrds_index = header.index("AVG NUMBER OF WORDS PER SENTENCE")
    cmpxwrd_count_index = header.index("COMPLEX WORD COUNT")
    wrd_count_index = header.index("WORD COUNT")
    syl_wrd_index = header.index("SYLLABLE PER WORD")
    per_pro_index = header.index("PERSONAL PRONOUNS")
    avg_wrd_len_index = header.index("AVG WORD LENGTH")
    data = [row for row in reader]

for row, result in zip(data, results):
    row[positive_index] = result[0]
    row[negative_index] = result[1]
    row[polarity_index] = result[2]
    row[subjectivity_index] = result[3]
    row[avg_sent_len_index] = result[4]
    row[per_cmplxwrds_index] = result[5]
    row[fog_ind_index] = result[6]
    row[avg_nowrds_index] = result[7]
    row[cmpxwrd_count_index] = result[8]
    row[wrd_count_index] = result[9]
    row[syl_wrd_index] = result[10]
    row[per_pro_index] = result[11]
    row[avg_wrd_len_index] = result[12]

with open("Output Data Structure.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(data)