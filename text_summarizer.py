import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from heapq import nlargest

# Download required resources (only first time)
nltk.download('punkt')
nltk.download('stopwords')

def summarize_text(text, summary_length=2):

    # Convert text into sentences
    sentences = sent_tokenize(text)

    # Convert text into words
    words = word_tokenize(text.lower())

    # Remove stopwords and punctuation
    stop_words = set(stopwords.words("english"))
    punctuation = set(string.punctuation)

    filtered_words = [
        word for word in words
        if word not in stop_words and word not in punctuation
    ]

    # Calculate word frequency
    word_freq = {}
    for word in filtered_words:
        word_freq[word] = word_freq.get(word, 0) + 1

    # Normalize word frequencies
    max_freq = max(word_freq.values()) if word_freq else 1
    for word in word_freq:
        word_freq[word] = word_freq[word] / max_freq

    # Score sentences
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_freq:
                if len(sentence.split()) < 30:  # Avoid very long sentences
                    sentence_scores[sentence] = sentence_scores.get(sentence, 0) + word_freq[word]

    # Select top sentences
    summary_sentences = nlargest(summary_length, sentence_scores, key=sentence_scores.get)

    return " ".join(summary_sentences)


# ------------------- MAIN PROGRAM -------------------

print("----- Automatic Text Summarizer -----\n")

text = input("Enter the text to summarize:\n")

summary = summarize_text(text, summary_length=2)

print("\n----- Short Summary -----\n")
print(summary)
