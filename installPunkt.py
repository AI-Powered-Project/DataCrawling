import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')