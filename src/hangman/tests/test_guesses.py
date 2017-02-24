__copyright__ = 'Copyright(c) Gordon Elliott 2017'

from collections import OrderedDict

from unittest import TestCase
from mock import patch

from hangman.guesses import letters_from_player


class TestLettersFromPlayer(TestCase):
    """ Test that letters_from_player() accumulates the guesses correctly, is case
        insensitive and asks the player for another letter when they enter one they
        guessed already.
    """

    def _configure_input_mock(self, mock_input, inputs):
        """ Helper function which configures the mock for the builtin input()
        """

        def input_guesses(prompt):
            return inputs.pop(0)

        mock_input.side_effect = input_guesses

    @patch('hangman.guesses.input')
    def test_guesses_accumulate(self, mock_input):
        """ Check that guesses are accumulated as expected
        """
        guess_fixture = OrderedDict((
            ('a', ['a']),
            ('b', ['a', 'b']),
            ('c', ['a', 'b', 'c']),
        ))

        self._configure_input_mock(mock_input, list(guess_fixture.keys()))

        for (expected_guess, expected_guesses), (guess, guesses) in zip(guess_fixture.items(), letters_from_player()):
            self.assertEqual(expected_guess, guess)
            self.assertEqual(expected_guesses, guesses)

    @patch('hangman.guesses.input')
    @patch('hangman.guesses.print')
    def test_duplicates_not_accepted(self, mock_print, mock_input):
        """ Verify that duplicates are not generated from the function
        """
        guess_fixture = OrderedDict((
            ('a', ['a']),
            ('b', ['a', 'b']),
            ('c', ['a', 'b', 'c']),
        ))

        self._configure_input_mock(mock_input, ['a', 'b', 'b', 'a', 'c'])

        for (expected_guess, expected_guesses), (guess, guesses) in zip(guess_fixture.items(), letters_from_player()):
            self.assertEqual(expected_guess, guess)
            self.assertEqual(expected_guesses, guesses)

        # check that the user is informed that they need to choose a different letter
        self.assertEqual(2, mock_print.call_count)

    @patch('hangman.guesses.input')
    @patch('hangman.guesses.print')
    def test_case_insensitive(self, mock_print, mock_input):
        """ Ensure that the case of the letters is preserved but ignored when checking for
            duplicates
        """
        guess_fixture = OrderedDict((
            ('A', ['A']),
            ('b', ['A', 'b']),
            ('C', ['A', 'b', 'C']),
        ))

        self._configure_input_mock(mock_input, ['A', 'b', 'B', 'a', 'C'])

        for (expected_guess, expected_guesses), (guess, guesses) in zip(guess_fixture.items(), letters_from_player()):
            self.assertEqual(expected_guess, guess)
            self.assertEqual(expected_guesses, guesses)
