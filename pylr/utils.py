# -*- coding: utf-8 -*-
''' Some utilities

    .. moduleauthor:: David Marteau <david.marteau@mappy.com>
    
'''


def enum(*sequential, **named):
    """ Create an enum type, as in the C language.
        You can, as i C, list names without any value, or set a value by using a named argument.
        But, of course, you cannot add unnamed arguments after named arguments...
        
        :param sequential: list of strings
        :param named: dictionnary of <strings:int value>
        :return: A new type created by using the params.
        :rtype: Enum  
    """
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


def signum(x):
    """ Give info about the sign of the given int.
    
        :param int x: Value whose sign is asked
        :return: -1 if the given value is negative, 0 if it is null, 1 if it is positive
        :rtype: int
    """
    return -1 if x < 0 else 0 if x == 0 else 1


class lazyproperty(object):
    """ Meant to be used as decorator for lazy evaluation of an object attribute.
        Property should represent non-mutable data, as it replaces itself.
    """
    def __init__(self, fget):
        self.fget = fget
        self.func_name = fget.__name__
        self.__doc__ = fget.__doc__

    def __get__(self, obj, cls):
        if obj is None:
            return None
        value = self.fget(obj)
        setattr(obj, self.func_name, value)
        return value
