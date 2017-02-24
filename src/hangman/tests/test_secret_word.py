__copyright__ = 'Copyright(c) Gordon Elliott 2017'

from unittest import TestCase
from mock import patch, mock_open

from hangman.secret_word import SecretWord, WordsNotFound


WORD_FIXTURES = (
    'first',
    'second',
    'third'
)


def mock_open_iterable(read_data=''):
    """ Improve on the standard mock_open() to make the returned mock iterable

    :param read_data: option string to mock file contents
    :return: mock file object
    """

    improved_mock_open = mock_open(read_data=read_data)
    improved_mock_open.return_value.__iter__ = lambda self: self
    improved_mock_open.return_value.__next__ = lambda self: next(iter(self.readline, ''))

    return improved_mock_open


class TestSecretWordFileErrors(TestCase):

    def test_pick_word_no_dictionary(self):
        with self.assertRaises(FileNotFoundError):
            secret = SecretWord('/unknown/file/path')
            secret.pick_word()

    @patch('hangman.secret_word.open', mock_open_iterable(read_data=''))
    def test_pick_word_empty_dictionary(self):
        with self.assertRaises(WordsNotFound):
            secret = SecretWord('/mock/file/path')
            secret.pick_word()


class TestSecretWord(TestCase):

    def setUp(self):
        super().setUp()
        self._secret = SecretWord('/mock/file/path')
        self._secret._secret_word = 'fixture word'

    @patch(
        'hangman.secret_word.open',
        mock_open_iterable(read_data='\n'.join(WORD_FIXTURES))
    )
    def test_pick_word_exists_in_dictionary(self):
        self._secret.pick_word()
        self.assertIn(self._secret._secret_word, WORD_FIXTURES)

    def test_compare_guesses_no_guesses(self):
        matches = self._secret.matching_guesses([])

        self.assertListEqual(
            ['_'] * len(self._secret._secret_word),
            matches
        )

    def test_compare_guesses_some_matches(self):
        matches = self._secret.matching_guesses('xtur')

        self.assertListEqual(
            ['_', '_', 'x', 't', 'u', 'r', '_', '_', '_', '_', 'r', '_'],
            matches
        )

    def test_compare_guesses_case_insensitive(self):
        self._secret._secret_word = 'Fixture Word'
        matches = self._secret.matching_guesses('XWtUr')

        self.assertListEqual(
            ['_', '_', 'x', 't', 'u', 'r', '_', '_', 'W', '_', 'r', '_'],
            matches
        )

    def test_last_guess_not_correct(self):
        self.assertFalse(self._secret.last_guess_was_correct)
        self._secret.matching_guesses('fre')
        self.assertFalse(self._secret.last_guess_was_correct)

    def test_last_guess_was_correct(self):
        self.assertFalse(self._secret.last_guess_was_correct)
        self._secret.matching_guesses('fixture wod')
        self.assertTrue(self._secret.last_guess_was_correct)

    def test_letter_not_in_secret(self):
        self.assertFalse(self._secret.contains('b'))

    def test_letter_in_secret(self):
        self.assertTrue(self._secret.contains('W'))
