"""
Importing libraries
"""
import logging
from difflib import SequenceMatcher

import requests
import argparse
from .exceptions import *
from .utils import *
import pprint

LOGGER = logging.getLogger("api")  # Initializing logger
LOGGER.setLevel(logging.DEBUG)  # Setting level to DEBUG


def main():
    """
    This method is used for the command line arguments  it can, will be executed when accessing
    it through the terminal / cmd / powershell

    usage: ExchangeRateApi [-h] -k KEY [-q QUOTA] [-l LATEST] [-c CURRENCY] [-p [PAIR [PAIR ...]]] [-e ENRICHED ENRICHED] [-H [HISTORICAL [HISTORICAL ...]]]
                       [-s [SEARCH [SEARCH ...]]]

    This library will allow the user to use the api functionality of ExchangeRateApi, it will make use of the request library in order to make the requests from
    the ExchangeRateApi.

    optional arguments:
    -h, --help            show this help message and exit
    -k KEY, --key KEY     Api key for the ExchangeRateApi
    -q QUOTA, --quota QUOTA
                            Gives the quota for the api key
    -l LATEST, --latest LATEST
                            Gives the latest exchange rate of the currency
    -c CURRENCY, --currency CURRENCY
                            Gives the supported codes
    -p [PAIR [PAIR ...]], --pair [PAIR [PAIR ...]]
                            Converts the first currency to the second currency and if any amount is given it will be converted to the specified amount Format -
                            Currency Currency Amount = 1
    -e ENRICHED ENRICHED, --enriched ENRICHED ENRICHED
                            Converts the first currency to the second currency and if any amount is given it will be converted to the specified amount and gives
                            the enriched data The information contains : - Country - Two-Letter Code - Currency Name - Currency Name short - Symbol - Flag Url
                            Format - Currency Currency
    -H [HISTORICAL [HISTORICAL ...]], --historical [HISTORICAL [HISTORICAL ...]]
                            Gives the historical data of the currency and users should provide date, month and year Format - Currency Date Month Year Amount = 1
    -s [SEARCH [SEARCH ...]], --search [SEARCH [SEARCH ...]]
                            Searches for the currency codes in order to give the valid currency code Format - Key is_country=0 Provide is_country as 1 if you
                            want to get the currency code for the country else leave it empty

    :return:  None
    """
    parser = argparse.ArgumentParser(prog="ExchangeRateApi",
                                     description="This library will allow the user to use the api functionality of ExchangeRateApi,"
                                                 " it will make use of the request library in order to make the requests from the ExchangeRateApi.")

    parser.add_argument("-k", "--key", type=str,
                        help="Api key for the ExchangeRateApi", required=True, nargs=1)

    parser.add_argument(
        "-q", "--quota", help="Gives the quota for the api key", action='store_true')

    parser.add_argument("-l", "--latest", type=str,
                        help="Gives the latest exchange rate of the currency", nargs=1)

    parser.add_argument("-c", "--currency",
                        help="Gives the supported codes", action='store_true')

    parser.add_argument("-p", "--pair", type=str, nargs='*',
                        help="Converts the first currency to the second currency and if any amount is given it will be converted to the specified amount\nFormat - Currency Currency Amount = 1")

    parser.add_argument("-e", "--enriched", type=str, nargs=2, help="Converts the first currency to the second currency and if any amount is given it will be converted to the specified amount and gives the enriched data\nThe information contains :\n- Country \n- Two-Letter Code\n- Currency Name\n- Currency Name short\n- Symbol\n- Flag Url\nFormat - Currency Currency")

    parser.add_argument("-H", "--historical", type=str, nargs='*',
                        help="Gives the historical data of the currency and users should provide date, month and year\nFormat - Currency Date Month Year Amount = 1")

    parser.add_argument("-s", "--search", type=str, nargs='*',
                        help="Searches for the currency codes in order to give the valid currency code\n"
                             "Format - Key is_country=0\nProvide is_country as 1 if you want to get the currency code for the country else leave it empty")

    args = parser.parse_args()

    key = args.key[0]
    api = ExchangeRateApi(key)
    if args.quota:
        print(api.get_quota())
    elif args.latest:
        pprint.pprint(api.get_latest(args.latest[0]))
    elif args.currency:
        pprint.pprint(api.get_codes())
    elif args.pair:
        let = args.pair
        if len(let) > 3:
            raise CliFormatError(
                "Format - Currency Currency Amount - is optional and should be integer")
        if len(let) == 2:
            let.append('1')
        print(api.get_pair_conversion(let[0].strip(), let[1], float(let[2])))
    elif args.enriched:
        let = args.enriched
        print(api.get_enriched_data(let[0].strip(), let[1]))
    elif args.historical:
        let = args.historical
        if len(let) > 5:
            raise CliFormatError(
                "Format - Currency Date Month Year Amount = 1 - is optional and should be integer")
        if len(let) == 4:
            let.append('1')
        pprint.pprint(api.get_historical_data(let[0].strip().upper(), int(let[1]), int(
            let[2]), int(let[3]), float(let[4])))
    elif args.search:
        let = args.search
        if len(let) > 2:
            raise CliFormatError(
                "Format - Key is_country=0\nProvide is_country as 1 if you want to get the currency code for the country else leave it empty")
        if len(let) == 1:
            let.append('0')
        if let[-1] == '0':
            api.search(let[0].strip())
        else:
            api.search(let[0].strip(), True)
    else:
        raise NoArgumentError(
            "No arguments have been passed\nUse -h or --help to get help on using cli")


class ExchangeRateApi:
    # TODO save api key
    # TODO To write unit tests
    # TODO To test cli
    """
    ExchangeRateApi
    --------------------
    This library will allow the user to use the api functionality of ExchangeRateApi, it will make use of the
    request library in order to make the requests from the ExchangeRateApi.

    Method
    -----------
     - get_latest(self, base_currency: str) -> dict
     - get_pair_conversion(self, from_currency: str, to_currency: str, amount: float = 1.0000) -> str
     - get_codes() -> dict
     - get_quota(self) -> str
     - get_enriched_data(self, from_currency: str, to_currency: str) -> str
     - get_historical_data(self, base_currency: str, date: int, month: int, year: int, amount: float = 1.0000) -> dict
     - search(key: str, is_country: bool = False, is_print: bool = True) -> list

    Exceptions
    ------------
     - InvalidKeyError
     - InactiveAccountError
     - QuotaExceededError
     - UnsupportedCodeError
     - MalformedRequestError
     - PlanUpgradeRequiredError
     - NoDataAvailableError

    :Authors: Tony Stark
    """

    def __init__(self, api_key: str):
        """
        This allows you to create an object of ExchangeRateApi with the api_key
        :param api_key: Your api key
        """
        self.api_key = api_key
        self.base_url = f"{URL}{self.api_key}"
        fh = logging.FileHandler("api.log", )
        fh.setLevel(logging.DEBUG)
        console = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(levelname)s] - [pid %(process)d] - %(asctime)s : %(message)s in %(module)2s.%("
            "funcName)2s()s at line number : %(lineno)d "
        )
        fh.setFormatter(formatter)
        console.setFormatter(
            logging.Formatter("[%(levelname)s] : %(message)s in the function %(funcName)2s() at line %(lineno)d"))
        console.setLevel(logging.ERROR)
        LOGGER.addHandler(fh)
        LOGGER.addHandler(console)
        LOGGER.info("API set")
        LOGGER.info("BASE URL set")

    def __check_errors(self, response: dict, *args) -> bool:
        """
        This method can't be directly called by the object instead they should call ExchangeRateApi_check_errors since the naming
        :param response: This should be the api response in json format
        :param args: This argument is optional
        :raise InvalidKeyError This raises when the api key is not valid
        :raise InactiveAccountError This raises when the account is not activated
        :raise QuotaExceededError This raises when quota of the api key is exceeded
        :raise UnsupportedCodeError This raises when the currency code is not supported
        :raise MalformedRequestError This raises when the url form is not a valid one
        :raise PlanUpgradeRequiredError This raises when you try to access the functions which can't be accessed from the current plan of the account
        :raise NoDataAvailableError This raises when you try to access the historical data with the data which isn't available
        :return: This method returns True if there is no errors else returns False
        :rtype: bool
        """
        new_line = "\n\t"
        if len(args) > 1 and (len(args[0]) != 3 or len(args[1]) != 3):
            raise UnsupportedCodeError(f"The currency code  used to invoke the api is not supported."
                                       f"\nUse the method get_codes() to get the supported codes\n"
                                       f"Did you mean:\n{args[0]}:\n\t{new_line.join(self.search(args[0], is_print=False))}\n"
                                       f"{args[1]}:\n\t{new_line.join(self.search(args[1], is_print=False))}\t \n- ")
        if response[RESULT] != "success":
            error_code = response[ERROR_TYPE]
            if error_code == "invalid-key":
                raise InvalidKeyError(
                    f"Your api key - {self.api_key} is not valid")
            elif error_code == "inactive-account":
                raise InactiveAccountError("Your account with the api key is not activated.\nMake sure your email has "
                                           "been confirmed")
            elif error_code == "quota-reached":
                raise QuotaExceededError(
                    "The api key has reached its quota for this month")
            elif error_code == "unsupported-code":
                raise UnsupportedCodeError(f"The currency code  used to invoke the api is not supported."
                                           f"\nUse the method get_codes() to get the supported codes\n"
                                           f"Did you mean:\n{args[0]}:\n\t{new_line.join(self.search(args[0], is_print=False))}\n"
                                           f"{args[1]}:\n\t{new_line.join(self.search(args[1], is_print=False))}\t \n- ")
            elif error_code == "malformed-request":
                raise MalformedRequestError(
                    f"The url - {args[2]} formats used in the api call has some errors")
            elif error_code == "plan-upgrade-required":
                raise PlanUpgradeRequiredError(
                    f"The function you are trying to call is not accessible with your account's plan")
            elif error_code == "no-data-available":
                raise NoDataAvailableError(
                    f"No data is available in the date {args[3]}/{args[4]}/{args[5]}")
            return False
        LOGGER.info("Api call has been invoked without any errors")
        return True

    def get_latest(self, base_currency: str) -> dict:
        """
        This method allows the user to get the latest exchange rate of the currency the user passes in the method
        :param base_currency: The currency should be in the three letter format, and it should be supported by theExchangeRateApi
        :return: It will return the dictionary with the exchange rates
        :rtype: dict
        """
        try:
            base_currency = base_currency.upper()
            url = f"{self.base_url}/latest/{base_currency}"
            response = requests.get(url).json()
            if self.__check_errors(response, base_currency, base_currency):
                return response[CONVERSION_RATES]

        except requests.exceptions.ConnectionError:
            LOGGER.error(f"There is no internet connections")
        except (InvalidKeyError, InactiveAccountError, QuotaExceededError, MalformedRequestError, UnsupportedCodeError,
                PlanUpgradeRequiredError, NoDataAvailableError) as e:
            LOGGER.error(e)
        except Warning as e:
            LOGGER.warning(e)
        except (Exception, KeyError, SyntaxError, ReferenceError, RuntimeError, SystemError, ValueError,
                KeyboardInterrupt, SystemExit) as e:
            LOGGER.error(e, exc_info=True)
        return {}

    def get_pair_conversion(self, from_currency: str, to_currency: str, amount: float = 1.0000) -> str:
        """
        This method is used to convert the base currency to the required currency. Amount is an optional argument the default will be 1
        :param from_currency: The currency code on which you want to be converted
        :param to_currency: The currency code on which the from_currency is converted
        :param amount: It is an optional argument. It is set to 1.0 at default. It is the amount of the from_currency to be converted to to_currency
        :return: It returns a string which contains the converted amount
        :rtype: str
        """
        try:
            from_currency = from_currency.upper()
            to_currency = to_currency.upper()
            if amount <= 0.0:
                LOGGER.error(f"Amount [{amount}] should be greater than one")
                return ""
            url = f"{self.base_url}/pair/{from_currency}/{to_currency}/{amount}"
            response = requests.get(url).json()
            if self.__check_errors(response, from_currency, to_currency, url):
                return f"\n ---- Pair Conversion ---- \n" \
                       f"{amount} {from_currency} [{CODES[from_currency]}] = " \
                       f"{response[CONVERSION_RESULTS]} {to_currency} [{CODES[to_currency]}]\n" \
                       f"Time last updated [unix] : {response[TIME_LAST_UPDATE_UNIX]}\n" \
                       f"Time last updated [utc] : {response[TIME_LAST_UPDATE_UTC]}\n" \
                       f"Time next update [unix] : {response[TIME_NEXT_UPDATE_UNIX]}\n" \
                       f"Time next update [utc] : {response[TIME_NEXT_UPDATE_UTC]}\n\n"
        except requests.exceptions.ConnectionError:
            LOGGER.error(f"There is no internet connections")
        except (InvalidKeyError, InactiveAccountError, QuotaExceededError, MalformedRequestError, UnsupportedCodeError,
                PlanUpgradeRequiredError, NoDataAvailableError) as e:
            LOGGER.error(e)
        except Warning as e:
            LOGGER.warning(e)
        except (Exception, KeyError, SyntaxError, ReferenceError, RuntimeError, SystemError, ValueError,
                KeyboardInterrupt, SystemExit) as e:
            LOGGER.error(e, exc_info=True)
        return ""

    @staticmethod
    def get_codes() -> dict:
        """
        This is a static method which allows the user to get the supported codes

        :return: Returns the supported currency codes of the api
        :rtype: dict
        """
        LOGGER.info("Valid currency triggered")
        return CODES

    def get_quota(self) -> str:
        """
        This method allows the user to get the quota of the account which is attached to the api key.\n
        The quota contains :
         - Total Quota
         - Quota Remaining
         - Refresh Day

        :return: Returns the quota information of the api key
        :rtype: str
        """
        try:
            url = f"{self.base_url}/quota"
            response = requests.get(url).json()
            if self.__check_errors(response):
                return f"\n ---- Quota ---- \n" \
                       f"Total Quota = {response[PLAN_QUOTA]}\n" \
                       f"Quota Remaining = {response[REQUEST_REMAINING]}\nQuota " \
                       f"Refresh Day = {response[REFRESH_DAY_OF_MONTH]}\n\n"
        except requests.exceptions.ConnectionError:
            LOGGER.error(f"There is no internet connections")
        except (InvalidKeyError, InactiveAccountError, QuotaExceededError, MalformedRequestError, UnsupportedCodeError,
                PlanUpgradeRequiredError, NoDataAvailableError) as e:
            LOGGER.error(e)
        except Warning as e:
            LOGGER.warning(e)
        except (Exception, KeyError, SyntaxError, ReferenceError, RuntimeError, SystemError, ValueError,
                KeyboardInterrupt, SystemExit) as e:
            LOGGER.error(e, exc_info=True)
        return ""

    def get_enriched_data(self, from_currency: str, to_currency: str) -> str:
        """
        This method allows the user to get the enriched data i.e. all the information about the to_currency.\n
        The information contains :
            - Country
            - Two-Letter Code
            - Currency Name
            - Currency Name short
            - Symbol
            - Flag Url
        :param from_currency: Currency code of the base currency
        :param to_currency: Currency code to get the enriched data
        :return: Returns all the enriched data of the currency code
        :rtype: str
        """

        try:
            url = f"{self.base_url}/enriched/{from_currency}/{to_currency}"
            response = requests.get(url).json()
            if self.__check_errors(response, from_currency, to_currency, url):
                target = response[TARGET_DATA]
                symbol = list(map(lambda x: (r"\u" + x).encode("utf-8").decode("unicode-escape"),
                                  target[CURRENCY_SYMBOL].split(",")))
                return f"\n ---- Enriched Data ---- \n" \
                       f"1 {from_currency} [{CODES[from_currency]}] = " \
                       f"{response[CONVERSION_RATE]} {to_currency} [{CODES[to_currency]}]\n" \
                       f"Country : {target[LOCALE]}\n" \
                       f"Two Letter Code : {target[TWO_LETTER_CODE]}\n" \
                       f"Currency Name : {target[CURRENCY_NAME]}\n" \
                       f"Currency Name Short : {target[CURRENCY_NAME_SHORT]}\n" \
                       f"Symbol : {''.join(symbol)}\n" \
                       f"Flag Url : {target[FLAG_URL]}\n" \
                       f"Time last updated [unix] : {response[TIME_LAST_UPDATE_UNIX]}\n" \
                       f"Time last updated [utc] : {response[TIME_LAST_UPDATE_UTC]}\n" \
                       f"Time next update [unix] : {response[TIME_NEXT_UPDATE_UNIX]}\n" \
                       f"Time next update [utc] : {response[TIME_NEXT_UPDATE_UTC]}\n\n"
        except requests.exceptions.ConnectionError:
            LOGGER.error(f"There is no internet connections")
        except (InvalidKeyError, InactiveAccountError, QuotaExceededError, MalformedRequestError, UnsupportedCodeError,
                PlanUpgradeRequiredError, NoDataAvailableError) as e:
            LOGGER.error(e)
        except Warning as e:
            LOGGER.warning(e)
        except (Exception, KeyError, SyntaxError, ReferenceError, RuntimeError, SystemError, ValueError,
                KeyboardInterrupt, SystemExit) as e:
            LOGGER.error(e, exc_info=True)
        return ""

    def get_historical_data(self, base_currency: str, date: int, month: int, year: int, amount: float = 1.0000) -> dict:
        """
        This method is used to get the historical data of the base currency and users should provide date, month and yearAmount is optional it will be defaulted to 1
        :param base_currency: Currency code on which you need to get the historical data
        :param date: The date on which you need to get the currency exchange rate
        :param month: The month on which you need to get the currency exchange rate
        :param year: The year on which you need to get the currency exchange rate
        :param amount: It is an optional argument.It is by default set to 1
        :return: Returns the exchange rates of the base currency at the given date, month and year
        :rtype: dict
        """
        try:
            url = f"{self.base_url}/history/{base_currency.upper()}/{year}/{month}/{date}/{amount}"
            response = requests.get(url).json()
            if self.__check_errors(response, base_currency, base_currency, url, date, month, year):
                return response[CONVERSION_AMOUNT]
        except requests.exceptions.ConnectionError:
            LOGGER.error(f"There is no internet connections")
        except (InvalidKeyError, InactiveAccountError, QuotaExceededError, MalformedRequestError, UnsupportedCodeError,
                PlanUpgradeRequiredError, NoDataAvailableError) as e:
            LOGGER.error(e)
        except Warning as e:
            LOGGER.warning(e)
        except (Exception, KeyError, SyntaxError, ReferenceError, RuntimeError, SystemError, ValueError,
                KeyboardInterrupt, SystemExit) as e:
            LOGGER.error(e, exc_info=True)
        return {}

    @staticmethod
    def search(key: str, is_country: bool = False, is_print: bool = True) -> list:
        """
        This method allows us to search the currency codes or can get the country name and provide with the currency codes
        :param key: Key element to search
        :param is_country: Whether the key element is a country or not
        :param is_print: Whether we need to print the found element
        :return: If opt not to print a list of matches will be returned
        """
        LOGGER.info("Function has been triggered")
        ele = CODES
        if is_country:
            ele = REVERSE_CODES
            key = key.capitalize()
        else:
            key = key.upper()
        maximum = 0
        matches = []
        is_present = False
        for keys in ele:
            similarity = SequenceMatcher(a=key, b=keys).ratio()
            if similarity != 0 and similarity >= maximum:
                if is_country and similarity >= 0.4:
                    is_present = True
                    if is_print:
                        print(f"{keys} - {ele[keys]}")
                    else:
                        matches.append(f"{keys} - {ele[keys]}")
                elif similarity >= 0.8:
                    is_present = True
                    if is_print:
                        print(f"{keys} - {ele[keys]}")
                    else:
                        matches.append(f"{keys} - {ele[keys]}")
                maximum = similarity
        if not is_print:
            return matches
        elif not is_present:
            print(f"There is no supported codes like - {key}")
