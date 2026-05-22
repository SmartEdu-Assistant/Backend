class EntityNotFoundError(Exception):
    def __init__(self, entity_name: str, entity_id: int) -> None:
        self.entity_name = entity_name
        self.entity_id = entity_id
        super().__init__(f'{entity_name} with id={entity_id} was not found')


class DomainValidationError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)
