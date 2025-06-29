from fastapi import HTTPException, status


def not_found_exception(detail: str = "Resource not found"):
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def validation_exception(detail: str = "Validation failed"):
    return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


def bad_request_exception(detail: str = "Bad request"):
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
