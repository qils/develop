#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import doctest


def import_object(name):
    '''
    imports object by name
    >>> import os.path
    >>> import_object('os.path') is os.path
    True
    >>> import_object('os.missing_module')
    Traceback (most recent call last):
        File "doc_test.py", line 30, in <module>
        import_object('os.missing_module')
        File "doc_test.py", line 25, in import_object
        raise ImportError('No module name {}'.format(parts[-1]))
    ImportError: No module name missing_module
    '''

    parts = name.split('.')
    obj = __import__('.'.join(parts[:-1]))

    try:
        return getattr(obj, parts[-1])
    except AttributeError:
        raise ImportError('No module name {}'.format(parts[-1]))


if __name__ == '__main__':
    doctest.testmod()
    # import_object('os.missing_module')

