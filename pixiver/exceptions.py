class PixivError(Exception):
    """ Base pixiv exception. """


class DateError(PixivError):
    """ Date range exception. """


class AjaxRequestError(Exception):
    """ Some unexpected errors may occur. """
