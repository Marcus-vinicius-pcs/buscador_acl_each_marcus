import unittest

from acl_search.search import matches_language, matches_query


class SearchTest(unittest.TestCase):
    def test_complete_query(self):
        self.assertTrue(
            matches_query("Opinion mining for stock price forecasting from tweets")
        )
        self.assertTrue(
            matches_query("Sentiment analysis for stock market prediction from Twitter")
        )

    def test_rejects_incomplete_query(self):
        self.assertFalse(matches_query("Sentiment signals for stock prediction from Twitter"))
        self.assertFalse(
            matches_query("Sentiment analysis predicts employee stock options from Twitter")
        )
        self.assertFalse(
            matches_query("Sentiment analysis for stock price forecasting from textual reports")
        )

    def test_language_filter(self):
        self.assertTrue(matches_language(None))
        self.assertTrue(matches_language("eng"))
        self.assertTrue(matches_language("pt"))
        self.assertFalse(matches_language("fr"))


if __name__ == "__main__":
    unittest.main()
