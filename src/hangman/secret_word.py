__copyright__ = 'Copyright(c) Gordon Elliott 2017'

from random import choice


NOT_GUESSED = '_'


class WordsNotFound(Exception):
    pass


class SecretWord(object):

    def __init__(self, words_filename):
        """ Constructor

        :param words_filename: string full path of file containing words to choose from
        """
        self._words_filename = words_filename
        self._secret_word = None
        self._last_guess_was_correct = False

    def pick_word(self):
        """ Pick a secret word
            random.choice() will fail with an IndexError if it is given
            an empty sequence to select from. Trap this exception and issue a
            custom exception.

        :return: string
        """
        try:
            with open(self._words_filename) as words_file:
                line = choice(list(words_file))
                self._secret_word = line.strip()
        except IndexError:
            raise WordsNotFound()

    def matching_guesses(self, guesses):
        """ Produce a list of characters, one for each of the letters in the secret
            word. Letters which match the guesses provided are shown; otherwise '_'
            is produced.

        :param guesses: list of characters
        :return: list of characters
        """
        self._last_guess_was_correct = True
        lower_case_guesses = list(map(lambda g: g.lower(), guesses))

        def matches(secret_letter):
            if secret_letter.lower() in lower_case_guesses:
                return secret_letter
            else:
                self._last_guess_was_correct = False
                return NOT_GUESSED

        matches = [
            matches(secret_letter)
            for secret_letter in self._secret_word
        ]

        return matches

    def contains(self, guess):
        """ Does the secret word contain the provided guess letter?

        :param guess: string guessed letter
        :return: bool
        """
        return guess.lower() in self._secret_word.lower()

    @property
    def last_guess_was_correct(self):
        """ Was the secret word guessed correctly with the last guess?

        :return: bool
        """
        return self._last_guess_was_correct

    def __str__(self):
        """ Output secret word

        :return: string
        """
        return self._secret_word
