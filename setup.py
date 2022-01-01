import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ExchangeRateApi",
    version="0.1.0",
    author="Tony Stark",
    author_email="manthirajak@gmail.com",
    description="This library uses the api functionality of ExchangeRateApi, it will make use of the request library in order to make the requests from the ExchangeRateApi.",
    packages=setuptools.find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TONYSTARK-EDITH/ExchangeRateApi.git",
    entry_points={
        'console_scripts': [
            'ExchangeRateApi = ExchangeRateApi.ExchangeRateApi:main'
        ]
    },
    keywords="ExchangeRate,ExchangeRateApi,python,terminal,ExchangeRates"
    ,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
