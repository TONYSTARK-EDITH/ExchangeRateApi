import unittest
from ExchangeRateApi import *
import requests

KEY = ExchangeRateApi("7a3b3053c9a3f73f72971358")


class MyTestCase(unittest.TestCase):

    def test_errors(self) -> None:
        KEY = ExchangeRateApi("7a3b3053c9a3f73f72971358asd")
        with self.assertRaises(tuple([InvalidKeyError, InactiveAccountError])):
            KEY._ExchangeRateApi__check_errors(requests.get(f"{KEY.base_url}/latest/INR").json(), "INR", "INR")
        KEY = ExchangeRateApi("7a3b3053c9a3f73f72971358")
        with self.assertRaises(UnsupportedCodeError):
            KEY._ExchangeRateApi__check_errors(requests.get(f"{KEY.base_url}/latest/IN").json(), "IN", "IN")
        with self.assertRaises(PlanUpgradeRequiredError):
            KEY._ExchangeRateApi__check_errors(requests.get(f"{KEY.base_url}/enriched/INR/USD").json(), "INR", "USD",
                                               f"{KEY.base_url}/enriched/INR/USD")


if __name__ == '__main__':
    unittest.main()
