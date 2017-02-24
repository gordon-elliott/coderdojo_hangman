__copyright__ = 'Copyright(c) Gordon Elliott 2017'

from unittest import TestCase

from hangman.gallows import Gallows


class TestGallows(TestCase):
    def test_template_init(self):
        template = '..{3}.{2}\n..{2}.{1}{0}'
        gallows = Gallows(template, 'abcd')

        self.assertEqual(4, gallows._num_stages)

    def test_multi_line_template(self):
        template = """
{5}{5}{4}
   {3}
{0}{1}{2}
"""
        gallows = Gallows(template, '___||-')

        self.assertEqual(6, gallows._num_stages)

    def test_stages_skipped_in_template(self):
        template = '{3}, {1}, '

        with self.assertRaises(AssertionError):
            Gallows(template, '_|')

    def test_stages_dont_match_template(self):

        with self.assertRaises(AssertionError):
            Gallows('{2},{1},{0}', '___*')

    def test_build_advances_current_stage(self):
        gallows = Gallows('{2}{0}{1}', '***')

        for s in (0, 1, 2):
            self.assertEqual(s, gallows._current_stage)
            gallows.build()

        self.assertTrue(gallows.is_complete)

    def test_reveal_by_stages(self):
        template = """
{3}{2}{2}
{3} {1}
{0}{0}{1}
"""
        stages = '_|-O'
        gallows = Gallows(template, stages, '.')

        expected_gallows = (
"""
...
. .
...
""",
"""
...
. .
__.
""",
"""
...
. |
__|
""",
"""
.--
. |
__|
""",
"""
O--
O |
__|
""",
        )

        for expected in expected_gallows:
            self.assertEqual(expected, gallows.reveal())
            gallows.build()

        self.assertTrue(gallows.is_complete)
