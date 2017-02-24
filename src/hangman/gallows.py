__copyright__ = 'Copyright(c) Gordon Elliott 2017'

import re


NOT_BUILT = ' '


class Gallows(object):
    """ Display a gallows using ascii art

        Segments of the gallows can progressively be included
    """

    def __init__(self, gallows_template, stages, not_built=NOT_BUILT):
        """ Constructor

        :param gallows_template: string template for the gallows
        :param stages: string characters used to fill stages of the gallows
        :param not_built: string used for gallows stages yet to be built
        """
        self._template = gallows_template
        self._stages = list(stages)
        self._not_built = not_built

        # validate the template - find the indices of the replacement parameters in the template
        stage_indices = set(map(int, re.findall(r'\{(\d+)\}', gallows_template)))
        self._num_stages = len(stage_indices)
        assert self._num_stages == len(self._stages), 'Template and stages string do not match'
        assert stage_indices == set(range(self._num_stages)), 'There are stages missing from the template'

        self._current_stage = 0

    def build(self):
        """ Advance the gallows to the next stage
        """
        if not self.is_complete:
            self._current_stage += 1

    @property
    def is_complete(self):
        """ Is the gallows complete?

        :return: bool
        """
        return self._current_stage == self._num_stages

    def reveal(self):
        """ Produce a view of the current state of the gallows

        :return: string
        """
        # take stages up to the current stage and concatenate with the the not built character
        # for the remaining stages
        stages = self._stages[:self._current_stage] + (
            [self._not_built,] * (self._num_stages - self._current_stage)
        )
        return self._template.format(*stages)


""" Gallows object to produce a classic image like this:

  ----|
  |  \|
  0   |
 /|\  |
  M   |
 / \  |
      |
 _____|__

"""

CLASSIC_GALLOWS = Gallows(
"""
  {3}{3}{3}{3}{1}
  {4}  {2}{1}
  {5}   {1}
 {7}{6}{8}  {1}
  {9}   {1}
 {10} {11}  {1}
      {1}
 {0}{0}{0}{0}{0}{1}{0}{0}
""",
    '_|\\-|0|/\\M/\\'
)
