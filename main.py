import argparse
import nltk
import pronouncing
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download('punkt')

def find_rhyming_sentences(text):
    sentences = sent_tokenize(text)
    word_to_sentence = {}
    
    for sentence in sentences:
        words = word_tokenize(sentence)
        if words:
            last_word = words[-1].lower()
            rhymes = pronouncing.rhymes(last_word)
            for rhyme in rhymes:
                if rhyme in word_to_sentence:
                    word_to_sentence[rhyme].append(sentence)
                else:
                    word_to_sentence[rhyme] = [sentence]
    
    return word_to_sentence

def create_poem_from_rhymes(word_to_sentence):
    used_sentences = set()
    poem = []
    
    for word, sentences in word_to_sentence.items():
        if len(sentences) > 1:
            for sentence in sentences:
                if sentence not in used_sentences:
                    poem.append(sentence)
                    used_sentences.add(sentence)
                    break

    return "\n".join(poem)

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("input", help="Input file to read the text from")
    args = args.parse_args()
    file_path = args.input
    print("Reading text from", file_path)
    print("Fisrt words are " + file_path[0:10] + "...)")
    with open(file_path, "r") as file:
        text = file.readlines()
        text = " ".join(text)


    word_to_sentence = find_rhyming_sentences(text)
    poem = create_poem_from_rhymes(word_to_sentence)

    print(poem)
