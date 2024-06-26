import argparse
import time
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
    used_rhymes = set()
    poem = []

    for word, phrases in word_to_phrase.items():
        if len(phrases) > 1:
            for phrase in phrases:
                last_word = phrase.split()[-1].lower()
                if (
                    phrase not in used_phrases
                    and last_word not in used_rhymes
                    and phrase_meter.get(phrase) == desired_meter
                ):
                    poem.append(phrase.strip())
                    used_phrases.add(phrase)
                    used_rhymes.add(last_word)
                    break

    return "\n".join(poem)


def read_multiple_files(file_paths):
    combined_text = ""
    for file_path in file_paths:
        with open(file_path, "r") as file:
            combined_text += file.read() + " "
    return combined_text.strip()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a rhyming poem from given text files."
    )
    parser.add_argument(
        "file_paths", metavar="F", type=str, nargs="+", help="paths to text files"
    )
    args = parser.parse_args()
    file_paths = args.file_paths

    text = read_multiple_files(file_paths)
    word_to_phrase, phrase_meter = find_rhyming_phrases(text)
    desired_meter = find_most_common_meter(phrase_meter)
    poem = create_poem_from_rhymes(word_to_phrase, phrase_meter, desired_meter)

    print(poem)
    with open("results/poem" + str(int(time.time())) + ".txt", "w") as file:
        file.write(poem)
