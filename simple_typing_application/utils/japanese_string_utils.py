
def is_hiragana(c: str) -> bool:
    '''Check if a character is a hiragana.

    Args:
        c (str): a character.

    Returns:
        bool: True if a character is a hiragana, otherwise False.

    Raises:
        ValueError: if len(c) != 1.

    Examples:
    >>> is_hiragana('あ')
    True
    >>> is_hiragana('ア')
    False
    >>> is_hiragana('a')
    False
    '''
    if len(c) != 1:
        raise ValueError(f'len(c) must be 1, but {len(c)}')
    return 'ぁ' <= c <= 'ゔ'


def delete_space_between_hiraganas(s: str) -> str:
    '''Delete spaces between hiraganas.

    Args:
        s (str): a string of hiraganas and spaces.

    Returns:
        str: a string of hiraganas without spaces.

    Examples:
    >>> s = 'こ んに ち は'
    >>> delete_space_between_hiraganas(s)
    'こんにちは'
    '''
    if len(s) <= 2:
        return s
    return (
        s[:1]
        + ''.join([
            b for a, b, c in zip(s[:-2], s[1:-1], s[2:])
            if not (is_hiragana(a) and is_hiragana(c) and b in [' ', '　'])
        ])
        + s[-1:]
    )
