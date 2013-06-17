__unittest = True


def assert_raises_assertion(*args, **kwargs):
    return assert_raises(AssertionError, *args, **kwargs)


def assert_raises(exception_class, message=None):
    class ContextManager(object):
        def __enter__(self):
            pass

        def __exit__(self, exc, exc_value, traceback):
            if exc_value is None:
                raise AssertionError(
                    'Expected to raise {}'.format(repr(exception_class)))
            elif isinstance(exc_value, exception_class):
                if message is not None:
                    if exc_value.message != message:
                        error_message = 'Expected {} == {}'.format(
                            repr(exc_value.message), repr(message))
                        raise AssertionError(error_message)
                return True
    return ContextManager()
