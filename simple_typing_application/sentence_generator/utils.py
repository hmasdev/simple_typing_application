import itertools
from ..const.hiragana_romaji_map import HIRA2ROMA_MAP, SMALL_HIRA2ROMA_MAP


def split_hiraganas_alphabets_symbols(s: str) -> list[str]:
    '''Split a string into a list of hiraganas, alphabets, and symbols.

    Args:
        s (str): a string of hiraganas, alphabets, and symbols.

    Returns:
        list[str]: a list of hiraganas, alphabets, and symbols.

    Examples:
    >>> s = 'HELLO、せかい！'
    >>> split_hiraganas_alphabets_symbols(s)
    ['H', 'E', 'L', 'L', 'O', '、', 'せ', 'か', 'い', '！']
    >>> s = 'こんにちは'
    >>> split_hiraganas_alphabets_symbols(s)
    ['こ', 'んに', 'ち', 'は']
    >>> s = 'あっというま'
    >>> split_hiraganas_alphabets_symbols(s)
    ['あ', 'っと', 'い', 'う', 'ま']
    >>> s = 'ふぁーぶる'
    >>> split_hiraganas_alphabets_symbols(s)
    ['ふぁ', 'ー', 'ぶ', 'る']
    >>> s = 'あっ、なんなん？'
    >>> split_hiraganas_alphabets_symbols(s)
    ['あ', 'っ、', 'な', 'んな', 'ん？']
    '''
    # split hiraganas into patterns
    patterns: list[str] = []
    pattern: list[str] = []
    for c, next_c in zip(s, s[1:]+' '):
        pattern.append(c)
        if c in ['っ', 'ん'] or next_c in SMALL_HIRA2ROMA_MAP:
            # NOTE: 'っ' and 'ん' requires the next character.
            # NOTE: keys of SMALL_HIRA2ROMA_MAP require the previous character.
            # See ../const/hiragana_romaji_map.py.
            continue
        else:
            patterns.append(''.join(pattern))
            pattern = []

    if c in ['っ', 'ん']:
        # Case: the sentence ends with 'っ' or 'ん'.
        patterns.append(''.join(pattern))
        pattern = []

    return patterns


def splitted_hiraganas_alphabets_symbols_to_typing_target(
    splitted_patterns: list[str],
) -> list[list[str]]:
    '''Convert a list of splitted hiraganas, alphabets, and symbols into a typing target.

    Args:
        splitted_patterns (list[str]): a list of splitted hiraganas, alphabets, and symbols.

    Returns:
        list[list[str]]: a typing target.

    Examples:
    >>> splitted_patterns = ['こ', 'んに', 'ち', 'は']
    >>> splitted_hiraganas_alphabets_symbols_to_typing_target(splitted_patterns)
    [['ko', 'co'], ['nnni', "n'ni", 'xnni'], ['ti', 'chi'], ['ha']]
    '''  # noqa

    # initialize
    typing_targets: list[list[str]] = []

    for pattern in splitted_patterns:

        # clean
        # zenkaku ascii -> hankaku ascii
        pattern = pattern.translate(str.maketrans(
            "#　！＂＃＄％＆＇（）＊＋，－．／０１２３４５６７８９：；＜＝＞？＠ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ［＼］＾＿｀ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ｛｜｝～￥",  # noqa
            "# !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~¥",  # noqa
        ))
        # zenkaku symbol -> hankaku symbol
        pattern = pattern.translate(str.maketrans(
            '、。・「」ー',
            ',./[]-',
        ))

        # pattern -> typing target
        if pattern.isascii() or pattern == '¥':
            # NOTE: pattern is typing target when pattern is ascii.
            typing_targets.append([pattern])

        elif pattern == 'ん':
            # Case: the sentence ends with 'ん'.
            typing_targets.append([c for c in HIRA2ROMA_MAP[pattern] if c != 'n' and c is not None])  # noqa

        elif pattern == 'っ':
            # Case: the sentence ends with 'っ'.
            typing_targets.append([c for c in HIRA2ROMA_MAP[pattern] if c is not None])  # noqa

        elif pattern in HIRA2ROMA_MAP:
            # NOTE: pattern is a key of typing target when pattern is in HIRA2ROMA_MAP.  # noqa
            # NOTE: Assume that HIRA2ROMA_MAP[pattern] does not contain None when pattern is in HIRA2ROMA_MAP.  # noqa
            typing_targets.append(HIRA2ROMA_MAP[pattern])  # type: ignore

        elif pattern.startswith('ん') or pattern.startswith('っ'):

            # initialize
            _target = []

            # split
            _splitted: list[str] = []
            for c in pattern:
                if c in SMALL_HIRA2ROMA_MAP:
                    _splitted[-1] += c
                else:
                    _splitted.append(c)

            # extract typing targets from candidates
            candidate: tuple[str | None, ...]
            for candidate in itertools.product(*[
                HIRA2ROMA_MAP[c] if c in HIRA2ROMA_MAP else [c]
                for c in _splitted
            ]):

                # preparation
                target_flag = True

                # check
                if candidate[-1] == 'n' or candidate[-1] is None:
                    target_flag = False
                    continue

                for s, t in zip(candidate, candidate[1:]):
                    if s is None and t is None:
                        # Example: 'tttu' -> 'ｔっつ'
                        target_flag = False
                        break
                    if s is None and t is not None and t[0] in ['a', 'i', 'u', 'e', 'o', 'n']:  # noqa
                        # Example: 'aa' -> not 'っあ' but 'ああ'
                        target_flag = False
                        break
                    if s is None and t is not None and not ('a' <= t[0] <= 'z' or 'A' <= t[0] <= 'Z'):  # noqa
                        # Example: ',,' -> not 'っ、' but '、、'
                        target_flag = False
                        break
                    if s == 'n' and t is not None and t[0] in ['a', 'i', 'u', 'e', 'o', 'n', 'y']:  # noqa
                        # Example: 'nna' -> not 'んな' but 'んあ'
                        target_flag = False
                        break

                # target registration
                if target_flag:
                    _target.append(''.join([
                        x if x is not None else y[0]  # type: ignore
                        # NOTE: when x is None, y is not None. See the above for-loop.  # noqa
                        for x, y in zip(candidate, candidate[1:] + (None,))
                    ]))

                # clean
                # TODO: improve this code
                if 'xxtsuto' in _target:
                    _target.remove('xxtsuto')  # NOTE: 'xxtsuto' -> 'ｘっと'
                if 'lltsuto' in _target:
                    _target.remove('lltsuto')  # NOTE: 'lltsuto' -> 'ｌっと'

            typing_targets.append(_target)

        else:
            raise ValueError(f'Invalid pattern: {pattern}')

    # check
    for targets in typing_targets:
        for target in targets:
            if 'ぁ' <= target <= 'ゔ':
                raise ValueError(f'Invalid typing target: {target}')

    return typing_targets
