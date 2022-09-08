class DadJokeClientError(Exception):
    """ Raised when there is an error in the dadjoke client """


class DadJokeClientHttpError(DadJokeClientError):
    """ Raised when an http error occurs in the dadjoke client """


class DadJokeClientNotFoundError(DadJokeClientHttpError):
    """ Raised when an entity is not found in the dadjoke client """
