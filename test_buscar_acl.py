import unittest

from buscar_acl import corresponde_a_string


class TesteDaBusca(unittest.TestCase):
    def test_string_completa(self):
        self.assertTrue(
            corresponde_a_string("Opinion mining for stock price forecasting from tweets")
        )
        self.assertTrue(
            corresponde_a_string(
                "Sentiment analysis for stock market prediction from Twitter"
            )
        )
        self.assertFalse(
            corresponde_a_string("Sentiment signals for stock prediction from Twitter")
        )
        self.assertFalse(
            corresponde_a_string(
                "Sentiment analysis predicts employee stock options from Twitter"
            )
        )
        self.assertFalse(
            corresponde_a_string(
                "Sentiment analysis for stock price forecasting from textual reports"
            )
        )


if __name__ == "__main__":
    unittest.main()
