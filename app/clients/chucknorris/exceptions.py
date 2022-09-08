class ChuckNorrisClientError(Exception):
    """ Raised when there is an error in the chucknorris client """


class ChuckNorrisClientHttpError(ChuckNorrisClientError):
    """ Raised when an http error occurs in the chucknorris client """


class ChuckNorrisClientNotFoundError(ChuckNorrisClientHttpError):
    """ Raised when an entity is not found in the chucknorris client """
