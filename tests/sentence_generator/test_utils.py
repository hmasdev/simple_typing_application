from __future__ import annotations
import pytest
from simple_typing_application.const import ASCII_CHARS
from simple_typing_application.sentence_generator.utils import (
    split_hiraganas_alphabets_symbols,
    splitted_hiraganas_alphabets_symbols_to_typing_target,
)


@pytest.mark.parametrize(
    "s,expected",
    [
        ("HELLO、せかい！", ['H', 'E', 'L', 'L', 'O', '、', 'せ', 'か', 'い', '！']),
        ("こんにちは", ['こ', 'んに', 'ち', 'は']),
        ("あっというま", ['あ', 'っと', 'い', 'う', 'ま']),
        ("ふぁーぶる", ['ふぁ', 'ー', 'ぶ', 'る']),
        ("あっ、なんなん？", ['あ', 'っ、', 'な', 'んな', 'ん？']),
        ("しょっく", ['しょ', 'っく']),
        (
            'あしたはあめがふるかもしれません',
            ['あ', 'し', 'た', 'は', 'あ', 'め', 'が', 'ふ', 'る', 'か', 'も', 'し', 'れ', 'ま', 'せ', 'ん'],  # noqa
        ),
        ('あっ', ['あ', 'っ']),
        # Unusual but acceptable cases
        ('っっ', ['っっ']),
        ('ふぁぁ', ['ふぁぁ']),  # NOTE: 'ふぁぁ' is not in HIRA2ROMA_MAP.
        ('あぁぁ', ['あぁぁ']),  # NOTE: 'あぁぁ' is not in HIRA2ROMA_MAP.
        ('っきゃぁ', ['っきゃぁ']),
        ('ぁぁ', ['ぁぁ']),
    ],
)
def test_split_hiraganas_alphabets_symbols(
    s: str,
    expected: list[str],
):
    actual: list[str] = split_hiraganas_alphabets_symbols(s)
    assert actual == expected


@pytest.mark.parametrize(
    "splitted_patterns,expected",
    [
        (
            ['H', 'e', 'l', 'l', 'o', '、', 'せ', 'か', 'い', '！'],
            [['H'], ['e'], ['l'], ['l'], ['o'], [','], ['se', 'ce'], ['ka', 'ca'], ['i', 'yi'], ['!']]  # noqa
        ),
        (
            ['こ', 'んに', 'ち', 'は', '。'],
            [['ko', 'co'], ['nnni', 'n\'ni', 'xnni'], ['ti', 'chi'], ['ha'], ['.']],  # noqa
        ),
        (
            ['あ', 'っと', 'い', 'う', 'ま'],
            [['a'], ['xtuto', 'xtsuto', 'ltuto', 'ltsuto', 'tto'], ['i', 'yi'], ['u', 'wu', 'whu'], ['ma']],  # noqa
        ),
        (
            ['ふぁ', 'ー', 'ぶ', 'る'],
            [['fa', 'huxa', 'hula', 'fuxa', 'fula'], ['-'], ['bu'], ['ru']],
        ),
        (
            ['あ', 'っ、', 'な', 'んな', 'ん？'],
            [['a'], ['xtu,', 'xtsu,', 'ltu,', 'ltsu,'], ['na'], ['nnna', 'n\'na', 'xnna'], ["nn?", "n'?", "xn?", 'n?']],  # noqa
        ),
        (
            ['しょ', 'っく'],
            [
                ["syo", "sho", "sixyo", "shixyo", "cixyo", "silyo", "shilyo", "cilyo"],  # noqa
                ["xtuku", "xtsuku", "ltuku", "ltsuku", 'kku', "xtucu", "xtsucu", "ltucu", "ltsucu", 'ccu', "xtuqu", "xtsuqu", "ltuqu", "ltsuqu", 'qqu'],  # noqa
            ],
        ),
        (
            list(ASCII_CHARS+"¥"),
            list(ASCII_CHARS+"¥"),
        ),
        (
            ['、', '。', '・', '「', '」', 'ー'],
            [[','], ['.'], ['/'], ['['], [']'], ['-']],
        ),
        (
            ['ぶ', 'んしょ', 'う'],
            [
                ['bu'],
                [
                    "nnsyo", "n'syo", "xnsyo", "nsyo",
                    "nnsho", "n'sho", "xnsho", "nsho",
                    "nnsixyo", "n'sixyo", "xnsixyo", "nsixyo",
                    "nnsilyo", "n'silyo", "xnsilyo", "nsilyo",
                    "nnshixyo", "n'shixyo", "xnshixyo", "nshixyo",
                    "nnshilyo", "n'shilyo", "xnshilyo", "nshilyo",
                    "nncixyo", "n'cixyo", "xncixyo", "ncixyo",
                    "nncilyo", "n'cilyo", "xncilyo", "ncilyo",
                ],
                ['u', 'wu', "whu"],
            ]
        ),
        (
            ['あ', 'し', 'た', 'は', 'あ', 'め', 'が', 'ふ', 'る', 'か', 'も', 'し', 'れ', 'ま', 'せ', 'ん'],  # noqa
            [
                ['a'], ['si', 'shi', 'ci'], ['ta'], [
                    'ha'], ['a'], ['me'], ['ga'],
                ['hu', 'fu'], ['ru'], ['ka', 'ca'], ['mo'],
                ['si', 'shi', 'ci'], ['re'], ['ma'], [
                    'se', 'ce'], ["nn", "n'", "xn"],
            ],
        ),
        (
            ['あ', 'っ'],
            [['a'], ['xtu', 'xtsu', 'ltu', 'ltsu']],
        ),
        (
            ['っっ'],
            [[
                # 'っ' and 'っと'
                'xtuxtu', 'xtuxtsu', 'xtultu', 'xtultsu',
                'xtsuxtu', 'xtsuxtsu', 'xtsultu', 'xtsultsu',
                'ltuxtu', 'ltuxtsu', 'ltultu', 'ltultsu',
                'ltsuxtu', 'ltsuxtsu', 'ltsultu', 'ltsultsu',
                # 　'っっ' and 'と'
                'xxtu',
                # 'xxtsu',  # NOTE: 'xxtsu' -> 'ｘっ'
                'lltu',
                # 'lltsu',  # NOTE: 'lltsu' -> 'ｌっ'
            ]]
        ),
        (
            ['っっと'],
            [[
                # 'っ' and 'っと'
                'xtuxtuto', 'xtuxtsuto', 'xtultuto', 'xtultsuto', 'xtutto',
                'xtsuxtuto', 'xtsuxtsuto', 'xtsultuto', 'xtsultsuto', 'xtsutto',  # noqa
                'ltuxtuto', 'ltuxtsuto', 'ltultuto', 'ltultsuto', 'ltutto',
                'ltsuxtuto', 'ltsuxtsuto', 'ltsultuto', 'ltsultsuto', 'ltsutto',  # noqa
                # 　'っっ' and 'と'
                'xxtuto',
                # 'xxtsuto',  # NOTE: 'xxtsuto' -> 'ｘっと'
                'lltuto',
                # 'lltsuto',  # NOTE: 'lltsuto' -> 'ｌっと'
            ]],
        ),
        (
            ['っあ'],
            [['xtua', 'xtsua', 'ltua', 'ltsua']],
        ),
        (
            ['んん'],
            [[
                'nxn', 'nnnn', "n'nn", "xnnn", "nnn'",
                "n'n'", "xnn'", 'nnxn', "n'xn", "xnxn",
            ]],
        ),
        # Unusual but acceptable cases
        (
            ['ふぁぁ'],
            [[
                'faxa', 'fuxaxa', 'huxaxa', 'fulaxa', 'hulaxa',
                'fala', 'fuxala', 'huxala', 'fulala', 'hulala',
            ]],
        ),  # NOTE: 'ふぁぁ' is not in HIRA2ROMA_MAP.
        (
            ['あぁぁ'],
            [['axaxa', 'alaxa', 'axala', 'alala']],
        ),  # NOTE: 'あぁぁ' is not in HIRA2ROMA_MAP.
        (
            ['っきゃぁ'],
            [[
                'kkyaxa', "xtukyaxa", "xtsukyaxa", "ltukyaxa", "ltsukyaxa",
                'kkixyaxa', "xtukixyaxa", "xtsukixyaxa", "ltukixyaxa", "ltsukixyaxa",  # noqa
                'kkilyaxa', "xtukilyaxa", "xtsukilyaxa", "ltukilyaxa", "ltsukilyaxa",  # noqa
                'kkyala', "xtukyala", "xtsukyala", "ltukyala", "ltsukyala",
                'kkixyala', "xtukixyala", "xtsukixyala", "ltukixyala", "ltsukixyala",  # noqa
                'kkilyala', "xtukilyala", "xtsukilyala", "ltukilyala", "ltsukilyala",  # noqa
            ]]
        ),
        (
            ['ぁぁ'],
            [['xaxa', 'laxa', 'xala', 'lala']],
        )
    ],
)
def test_splitted_hiraganas_alphabets_symbols_to_typing_target(
    splitted_patterns: list[str],
    expected: list[list[str]],
):
    actual: list[list[str]] = splitted_hiraganas_alphabets_symbols_to_typing_target(splitted_patterns)  # noqa

    # sort the list of list
    # NOTE: the order of the list of list is not important.
    expected_sorted = [sorted(x) for x in expected]
    actual_sorted = [sorted(x) for x in actual]

    assert actual_sorted == actual  # NOTE: check the order of the list of list
    assert actual_sorted == expected_sorted


def test_splitted_hiraganas_alphabets_symbols_to_typing_target_raise_error():
    with pytest.raises(ValueError):
        splitted_hiraganas_alphabets_symbols_to_typing_target(['β'])
