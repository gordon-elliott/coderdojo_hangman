__copyright__ = 'Copyright(c) Gordon Elliott 2017'


def letters_from_player():
    """ Generate a sequence of guesses from the player

    :yields: tuple of the latest guess and a list of all guesses so far
    """
    guesses = []
    while True:
        guess = None
        while guess is None or guess.lower() in map(lambda g: g.lower(), guesses):
            if guess and guesses:
                print('So far you have guessed {}.'.format(' '.join(guesses)))
            guess = input('What letter do you guess? ')

        guesses.append(guess)
        yield guess, guesses