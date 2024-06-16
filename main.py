import argparse
import nltk
import pronouncing
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download("punkt")


def get_meter(phrase):
    words = word_tokenize(phrase)
    stresses = [
        pronouncing.stresses_for_word(word.lower())
        for word in words
        if pronouncing.stresses_for_word(word.lower())
    ]
    if stresses:
        combined_stresses = "".join(stresses[0])
        return combined_stresses
    return ""


def tokenized_phrases_generator(text):
    sentences = sent_tokenize(text)
    for sentence in sentences:
        for phrase in sentence.split(","):
            yield phrase


def find_rhyming_phrases(text):
    word_to_phrase = {}
    phrase_meter = {}

    for phrase in tokenized_phrases_generator(text):
        words = word_tokenize(phrase)
        if words:
            last_word = words[-1].lower()
            rhymes = pronouncing.rhymes(last_word)
            for rhyme in rhymes:
                if rhyme in word_to_phrase:
                    word_to_phrase[rhyme].append(phrase)
                else:
                    word_to_phrase[rhyme] = [phrase]
        meter = get_meter(phrase)
        if meter:
            phrase_meter[phrase] = meter

    return word_to_phrase, phrase_meter


def find_most_common_meter(phrase_meter):
    meter_count = {}
    for meter in phrase_meter.values():
        if meter in meter_count:
            meter_count[meter] += 1
        else:
            meter_count[meter] = 1
    most_common_meter = max(meter_count, key=meter_count.get)
    return most_common_meter


def create_poem_from_rhymes(word_to_phrase, phrase_meter, desired_meter):
    used_phrases = set()
    poem = []

    for word, phrases in word_to_phrase.items():
        if len(phrases) > 1:
            for phrase in phrases:
                if (
                    phrase not in used_phrases
                    and phrase_meter.get(phrase) == desired_meter
                ):
                    poem.append(phrase.strip())
                    used_phrases.add(phrase)
                    break

    return "\n".join(poem)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("input", help="Input file to read the text from")
    args = args.parse_args()
    file_path = args.input
    print("Reading text from", file_path)
    print("First words are " + file_path[0:10] + "...)")
    with open(file_path, "r") as file:
        text = file.readlines()
        text = " ".join(text)

    word_to_phrase, phrase_meter = find_rhyming_phrases(text)
    desired_meter = find_most_common_meter(phrase_meter)
    poem = create_poem_from_rhymes(word_to_phrase, phrase_meter, desired_meter)

    print(poem)
