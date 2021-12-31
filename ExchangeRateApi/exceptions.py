class InvalidKeyError(AttributeError):
    """
    Invokes when the api key is invalid
    """

    def __init__(self, message):
        super(InvalidKeyError, self).__init__(message)


class InactiveAccountError(AttributeError):
    """
    Invokes when the account is not confirmed
    """

    def __init__(self, message):
        super(InactiveAccountError, self).__init__(message)


class QuotaExceededError(RuntimeError):
    """
    Invokes when quota of your api exceeds
    """

    def __init__(self, message):
        super(QuotaExceededError, self).__init__(message)


class UnsupportedCodeError(AttributeError):
    """
    Invokes when the currency code provided is not supported
    """

    def __init__(self, message):
        super(UnsupportedCodeError, self).__init__(message)


class MalformedRequestError(RuntimeError):
    """
    Invokes when there is a malformed request
    """

    def __init__(self, message):
        super(MalformedRequestError, self).__init__(message)


class PlanUpgradeRequiredError(AttributeError):
    """
    Invokes when you try to call a function which is not included in your current plan
    """

    def __init__(self, message):
        super(PlanUpgradeRequiredError, self).__init__(message)


class NoDataAvailableError(AttributeError):
    """
    Invokes when there is no data available when invoking historical data
    """

    def __init__(self, message):
        super(NoDataAvailableError, self).__init__(message)


class CliFormatError(AttributeError):
    """
    Invokes when there is more number of arguments than expected in cli
    """

    def __init__(self, message):
        super(CliFormatError, self).__init__(message)


class NoArgumentError(AttributeError):
    """
    Invokes when there is no argument passed in cli
    """

    def __init__(self, message):
        super(NoArgumentError, self).__init__(message)
