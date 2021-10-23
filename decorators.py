import functools

from db import database


def managed_transaction(func):

    @functools.wraps(func)
    def middleware(request, *args, **kwargs):
        session = database.get_session()
        try:
            request.session = session
            response = func(request, *args, **kwargs)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        return response

    return middleware
