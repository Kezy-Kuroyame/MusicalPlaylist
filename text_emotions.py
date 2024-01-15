from nltk import WordNetLemmatizer
from keras.models import load_model
import re
from keras.preprocessing.sequence import pad_sequences
import numpy as np
import nltk
from nltk.corpus import stopwords
import pickle
import pandas as pd
from keras.models import model_from_json


stop_words = set(stopwords.words('english'))


def remove_stop_words(text):
    Text = [i for i in str(text).split() if i not in stop_words]
    return " ".join(Text)


def Removing_numbers(text):
    text = ''.join([i for i in text if not i.isdigit()])
    return text


def lower_case(text):
    text = text.split()

    text = [y.lower() for y in text]

    return " ".join(text)


def Removing_punctuations(text):
    ## Remove punctuations
    text = re.sub('[%s]' % re.escape("""!"#$%&'()*+,،-./:;<=>؟?@[\]^_`{|}~"""), ' ', text)
    text = text.replace('؛', "", )

    ## remove extra whitespace
    text = re.sub('\s+', ' ', text)
    text = " ".join(text.split())
    return text.strip()


def Removing_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)


def lemmatization(text):
    lemmatizer = WordNetLemmatizer()

    text = text.split()

    text = [lemmatizer.lemmatize(y) for y in text]

    return " ".join(text)


def normalized_sentence(sentence):
    sentence = lower_case(sentence)
    sentence = remove_stop_words(sentence)
    sentence = Removing_numbers(sentence)
    sentence = Removing_punctuations(sentence)
    sentence = Removing_urls(sentence)
    sentence = lemmatization(sentence)
    return sentence


def text_emotions(sentence):
    # Загрузка сохраненной модели
    with open('models/emotion_model_architecture.json', 'r') as f:
        loaded_model = model_from_json(f.read())

    loaded_model.load_weights('models/emotion_model_weights.h5')

    with open('tokenizers/tokenizer2.pickle', 'rb') as handle:
        loaded_tokenizer = pickle.load(handle)

    y = ['empty', 'sadness', 'enthusiasm', 'neutral', 'worry', 'surprise',
         'love', 'fun', 'hate', 'happiness', 'boredom', 'relief', 'anger']
    labels = pd.get_dummies(y)

    # Токенизация
    new_sequences = loaded_tokenizer.texts_to_sequences([sentence])

    # Паддинг для выравнивания длины последовательностей
    new_padded_sequences = pad_sequences(new_sequences, maxlen=37, padding='post')

    # Предсказание эмоции
    predictions = loaded_model.predict(new_padded_sequences)

    # Получение наиболее вероятного класса (эмоции) для каждого текста
    predicted_label = labels.columns[np.argmax(predictions)]

    print(f"{sentence}: {predicted_label}")
    return predicted_label


    #
    # with open('tokenizers/tokenizer.pickle', 'rb') as handle:
    #     tokenizer = pickle.load(handle)
    # model = load_model('models/emotion_model.h5')
    # sentence = normalized_sentence(sentence)
    # sentence = tokenizer.texts_to_sequences([sentence]) # разделения текста на более мелкие единицы, такие как слова или подстроки (токены)
    # sentence = pad_sequences(sentence, maxlen=229, truncating='pre')
    # with open('labelencoders/le.pickle', 'rb') as handle:
    #     le = pickle.load(handle)
    # result = le.inverse_transform(np.argmax(model.predict(sentence), axis=-1))[0]
    # proba = np.max(model.predict(sentence))
    # print(f"{result} : {proba}\n\n")
    # return result
