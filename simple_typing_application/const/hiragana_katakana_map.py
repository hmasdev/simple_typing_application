
HIRAGANA: tuple[str, ...] = tuple(map(chr, range(0x3041, 0x3096 + 1)))
KATAKANA: tuple[str, ...] = tuple(map(chr, range(0x30A1, 0x30F6 + 1)))

HIRAGANA2KATAKANA_MAP: dict[str, str] = dict(zip(HIRAGANA, KATAKANA))
KATAKANA2HIRAGANA_MAP: dict[str, str] = dict(zip(KATAKANA, HIRAGANA))
