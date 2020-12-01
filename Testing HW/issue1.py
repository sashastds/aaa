def test_encode(message: str) -> str:
    """
    >>> test_encode(message='SOS')
    '... --- ...'
    >>> test_encode(message='')
    ''
    >>> test_encode(message='OSOSO') #doctest: +ELLIPSIS
    '---...---'
    >>> test_encode(message='SOS' * 20) 
    '... --- ... ... --- ... ... --- ... ... --- ... ... --- ... ... --- ... ... --- ... ... --- ... ... --- ... ... --- ...
    ... --- ... ... --- ... ... --- ... ... --- ... ... --- ... ... --- ... ... --- ... ... --- ... ... --- ... ... --- ...'
    >>> test_encode(message='sos')
    Traceback (most recent call last):
    ...
    KeyError: 's'
    """
    from morse import encode

    return encode(message)