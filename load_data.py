import typing as tp
import numpy as np


class CodeNamesData:
    def __init__(self, path: str):
        """
        :param path: path to data file
        """
        with open(path, 'r') as file:
            data = file.read()

        process_data = [category.split() for category in data.split('-')]
        mapping = {category[0]: list(
            map(lambda x: x.lower(), category[1:])) for category in process_data[1:]}
        self.categories = list(mapping.keys())
        self.vocabulary = []
        for category in mapping.values():
            for word in category:
                self.vocabulary.append(word.lower())
        self.mapping = mapping
        self.partitions = [(3, 3, 2), (4, 3, 1), (4, 2, 2),
                           (2, 2, 2, 2), (3, 3, 1, 1)]

    def sample_field(self) -> tp.Dict[str, tp.Union[tp.Dict['str', tp.List]], tp.List, str]:
        """
        Samples game field
        :return: returns a dictionary witch represents game field.
                 :key blue: contains dictionaries with mappings 'category name' -> list of words from category
                 :key neutral: contains list of neutral words
                 :key black: contains black word
        """
        field = {'blue': {}}
        part = np.random.choice(self.partitions)
        blue_categories = np.random.choice(
            self.categories, size=len(part), replace=False)
        for i, category in enumerate(blue_categories):
            words = np.random.choice(
                self.mapping[category], size=part[i], replace=False)
            field['blue'][category] = list(words)
        other_categories = set(self.categories) - set(blue_categories)
        other_vocab = []
        for category in other_categories:
            other_vocab.extend(self.mapping[category])
        other_words = np.random.choice(other_vocab, size=17, replace=False)
        field['neutral'] = list(other_words[1:])
        field['black'] = other_words[0]
        return field
