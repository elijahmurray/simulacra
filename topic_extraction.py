import gensim
from gensim.models import LdaMulticore
from gensim.corpora import Dictionary
from gensim.utils import simple_preprocess

def extract_topics(content, num_topics=5):
    # Tokenize the text
    tokens = simple_preprocess(content)
    
    # Create a dictionary from the tokens
    dictionary = Dictionary([tokens])
    
    # Create a bag of words representation of the text
    bow_corpus = [dictionary.doc2bow(tokens)]
    
    # Train an LDA model on the bag of words corpus
    lda_model = LdaMulticore(bow_corpus, num_topics=num_topics, id2word=dictionary)
    
    # Extract the top N topics and their scores from the LDA model
    topics = lda_model.show_topics(num_topics=num_topics, formatted=False)
    top_topics = [(topic[0], topic[1][0][0], topic[1][0][1]) for topic in topics]
    
    return top_topics
