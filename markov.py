import re
import random


class MarkovTextGenerator(object):
    #def __init__(self):

    def train(self, training_set):
        """
        Train the Markov Text Generator
        :param training_set: the input to use to train the generator. Can either be a string representing the entire corpus,
        or a list of filenames which contain text which will be used
        :return: None
        """

        if isinstance(training_set, str):
            raw_text = training_set
        elif isinstance(training_set, list):
            text_list = []
            for ts in training_set:
                if not isinstance(ts, str):
                    raise ValueError("The list passed in must contain strings")
                # get the file contents and add it to the list
                with open(ts, 'r') as f:
                    text_list.append(''.join(f.readlines()))
            # make one text corpus from the passed-in files
            raw_text = ''.join(text_list)
        else:
            raise ValueError("The training_set parameter must be a string or a list of filenames")

        # extract words
        self._word_list = self._extract_list(raw_text)
        # extract triplets
        self._words = self._generate_triples(self._word_list)

    def _extract_list(self, raw_text):
        """
        Extract individual words from raw text.
        New lines are first-class citizens and are treated like words.
        :param raw_text: the text to use
        :return: the extracted list of words
        """
        # find all lines of text or new lines
        text_only = re.sub(r'[^.a-zA-Z0-9 \n]', '', raw_text)
        m = re.findall('([a-z| ]+|\n)', text_only, re.MULTILINE | re.IGNORECASE)
        # m is a list of entire rows and new lines
        # use nested list comprehension to split each line into words, and concatenate with new lines
        return [item.lower() for sublist in [x.split(' ') for x in m] for item in sublist]

    def _generate_triples(self, word_list):
        """
        Extract word triples into a dictionary with key-value pairs of the form:
        (word1,word2): [word_list] where the key is a tuple and the value is a list of words
        that appear after the two words in the key.
        The list will act as a proxy for the transition probabilities, because the frequency of words in the list
        represent their frequency in the text. Sampling uniformly from this list will respect the transition
        probabilities
        :param word_list: the list of words to use
        :return: a dictionary of form (word1, word2): [words]
        """
        d = {}
        # loop through the text and generate triples
        for i in range(len(word_list)):
            if i == 0 or i == len(word_list) - 1:
                continue
            else:
                if (word_list[i-1], word_list[i]) in d:
                    d[(word_list[i-1], word_list[i])].append(word_list[i+1])
                else:
                    d[(word_list[i-1], word_list[i])] = []
                    d[(word_list[i-1], word_list[i])].append(word_list[i+1])
        return d

    def get_random_pair(self):
        """
        Return a random pair of words found in the main text
        :return: a list containing 2 strings
        """
        pair = random.choice(list(self._words))
        return [pair[0], pair[1]]

    def get_random_word(self, phrase=None):
        """
        Return the next word in a given phrase, or if not supplied then a word at random from the text
        :param phrase: an optional phrase to continue
        :return: a single string
        """
        if phrase:
            # find a phrase from the list of words associated with the last two words in the supplied phrase
            phrase_words = [x.lower() for x in phrase.split(' ')]
            if len(phrase_words) > 1:
                if (phrase_words[-2], phrase_words[-1]) in self._words:
                    past = self._words[(phrase_words[-2], phrase_words[-1])]
                else:
                    past = self._words[random.choice(list(self._words.keys()))]
            else:
                past = self._words[random.choice(list(self._words.keys()))]
        else:
            # no phrase supplied, return a word from our dict at random
            past = self._words[random.choice(list(self._words.keys()))]
        return random.choice(past)

    def generate_text(self, start_phrase='', text_size=50):
        """ Generate random text
        :param start_phrase: optional phrase to start the text with
        :param text_size: maximum number of words (default is 50)
        :return: the generated text
        """
        text = []
        if start_phrase == '':
            # if no starting text supplied, start with a random pair
            text.extend(self.get_random_pair())
        else:
            start_words = start_phrase.split(' ')
            # if two or more words were supplied
            if len(start_words) > 1:
                # the generated text will start with the starting phrase
                text.extend(start_words)
            else:
                text.extend(self.get_random_pair())
        # keep adding text until we reach the limit
        n_iterations = text_size - len(text)
        if(n_iterations > 0):
            for _ in range(n_iterations):
                text.extend([self.get_random_word(' '.join([text[-2], text[-1]]))])

        # return the text as a string
        return ' '.join(text)
