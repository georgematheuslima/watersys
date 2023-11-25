class ClientAlreadyRegistered(Exception):
    """Raised when the user tries to register a client with cpf that already exists in the database"""