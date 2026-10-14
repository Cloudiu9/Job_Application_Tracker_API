class ApplicationNotFoundError(Exception):
    """Missing resource. (404)"""
    pass

class ValidationError(Exception):
    """Invalid data. (400)"""
    pass
