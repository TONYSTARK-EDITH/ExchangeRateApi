# Exchange Rate Api

Welcome String is a Python library will allow to use the api functionality of ExchangeRateApi, it will make use of the
request library in order to make the requests from the ExchangeRateApi.<br>
https://www.exchangerate-api.com/

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Welcome-String.

```bash
pip install exchangerateapi
```

## Usage

The ExchangeRateApi takes 1 argument

```python
# Initialize an object to ExchangeRateApi
from ExchangeRateApi import *

api = ExchangeRateApi("YOUR_API_KEY")
```

There are 7 methods

<ol>
    <li>
      get_latest
    </li>
    <LI>get_pair_conversion</LI>
    <li>get_codes</li>
    <li>get_quota</li>
    <li>get_enriched_data</li>
    <li>get_historical_data</li>
    <li>search</li>
</ol>

```python
from ExchangeRateApi import *
import pprint

api = ExchangeRateApi("YOUR_API_KEY")

pprint.pprint(api.get_latest("INR"))  # get_latest method returns a dictionary

print(api.get_pair_conversion("INR", "USD", 2.0)) # get_pair_conversion returns a string

pprint.pprint(api.get_codes()) # get_codes returns a dictionary

print(api.get_quota()) # get_quota returns a string

print(api.get_enriched_data("INR","USD")) # get_enriched_data returns a string

pprint.pprint(api.get_historical_data("INR",20,12,2000,2.0)) # get_historical_data returns a dictionary

api.search("in") # returns a dictionary if is_print is False
```

## Features
- ## **Exception**

  New exceptions has been included
  - InvalidKeyError
  - InactiveAccountError
  - QuotaExceededError
  - UnsupportedCodeError
  - MalformedRequestError
  - PlanUpgradeRequiredError
  - NoDataAvailableError
  - CliFormatError
  - NoArgumentError


- ## **Command Line Interface**

  Command line interface has been added to this package

  ```bash
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
  ```

  <img src="https://drive.google.com/uc?export=view&id=1dXPaeYrGS3Rj7EiGlZimhVJeyPEwmgdU" alt="cli" style="zoom:150%;" />

  <img src="https://drive.google.com/uc?export=view&id=1Co-WTym1lZm5Zk3P3jd5X-zh1oOar6Gr" style="zoom:150%;"  alt="cli-optional" />

Test cases has been included

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://github.com/TONYSTARK-EDITH/ExchangeRateApi/blob/934b1406451f5fcaaeb5da7462ad5ea59909847c/LICENSE.md)
