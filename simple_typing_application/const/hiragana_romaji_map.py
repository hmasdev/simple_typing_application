from __future__ import annotations
from itertools import product


# TODO: make the maps immutable

HIRA2ROMA_MAP: dict[str, list[str | None]] = {
    # 50-on 50音
    "あ": ["a"],
    "い": ["i", "yi"],
    "う": ["u", "wu", "whu"],
    "え": ["e"],
    "お": ["o"],  # noqa
    "か": ["ka", "ca"],
    "き": ["ki"],
    "く": ["ku", "cu", "qu"],
    "け": ["ke"],
    "こ": ["ko", "co"],  # noqa
    "さ": ["sa"],
    "し": ["si", "shi", "ci"],
    "す": ["su"],
    "せ": ["se", "ce"],
    "そ": ["so"],  # noqa
    "た": ["ta"],
    "ち": ["ti", "chi"],
    "つ": ["tu", "tsu"],
    "て": ["te"],
    "と": ["to"],  # noqa
    "な": ["na"],
    "に": ["ni"],
    "ぬ": ["nu"],
    "ね": ["ne"],
    "の": ["no"],  # noqa
    "は": ["ha"],
    "ひ": ["hi"],
    "ふ": ["fu", "hu"],
    "へ": ["he"],
    "ほ": ["ho"],  # noqa
    "ま": ["ma"],
    "み": ["mi"],
    "む": ["mu"],
    "め": ["me"],
    "も": ["mo"],  # noqa
    "や": ["ya"],
    "ゆ": ["yu"],
    "いぇ": ["ye"],
    "よ": ["yo"],  # noqa
    "ら": ["ra"],
    "り": ["ri"],
    "る": ["ru"],
    "れ": ["re"],
    "ろ": ["ro"],  # noqa
    "わ": ["wa"],
    "を": ["wo"],
    "ん": [
        "nn",
        "n",
        "n'",
        "xn",
    ],  # NOTE: "n" is valid for 'ん' when the next character is not in "a", "i", "u", "e", "o", "n", "y".  # noqa
    # Dakuon/Handakuon 濁音/半濁音
    "ゔ": ["vu"],  # noqa
    "が": ["ga"],
    "ぎ": ["gi"],
    "ぐ": ["gu"],
    "げ": ["ge"],
    "ご": ["go"],  # noqa
    "ざ": ["za"],
    "じ": ["zi", "ji"],
    "ず": ["zu"],
    "ぜ": ["ze"],
    "ぞ": ["zo"],  # noqa
    "だ": ["da"],
    "ぢ": ["di"],
    "づ": ["du"],
    "で": ["de"],
    "ど": ["do"],  # noqa
    "ば": ["ba"],
    "び": ["bi"],
    "ぶ": ["bu"],
    "べ": ["be"],
    "ぼ": ["bo"],  # noqa
    "ぱ": ["pa"],
    "ぴ": ["pi"],
    "ぷ": ["pu"],
    "ぺ": ["pe"],
    "ぽ": ["po"],  # noqa
    # Yohon/拗音
    "うぁ": ["wha"],
    "うぃ": ["wi", "whi"],
    "うぇ": ["we", "whe"],
    "うぉ": ["who"],  # noqa
    "ゔぁ": ["va"],
    "ゔぃ": ["vi"],
    "ゔぇ": ["ve"],
    "ゔぉ": ["vo"],  # noqa
    "きゃ": ["kya"],
    "きぃ": ["kyi"],
    "きゅ": ["kyu"],
    "きぇ": ["kye"],
    "きょ": ["kyo"],  # noqa
    "ぎゃ": ["gya"],
    "ぎぃ": ["gyi"],
    "ぎゅ": ["gyu"],
    "ぎぇ": ["gye"],
    "ぎょ": ["gyo"],  # noqa
    "くぁ": ["qa", "qwa", "kwa"],
    "くぃ": ["qi", "qwi"],
    "くぅ": ["qu", "qwu"],
    "くぇ": ["qe", "qwe"],
    "くぉ": ["qo", "qwo"],  # noqa
    "ぐぁ": ["gwa"],
    "ぐぃ": ["gwi"],
    "ぐぅ": ["gwu"],
    "ぐぇ": ["gwe"],
    "ぐぉ": ["gwo"],  # noqa
    "くゃ": ["qya"],
    "くゅ": ["qyu"],
    "くょ": ["qyo"],  # noqa
    "しゃ": ["sya", "sha"],
    "しぃ": ["syi"],
    "しゅ": ["syu", "shu"],
    "しぇ": ["sye", "she"],
    "しょ": ["syo", "sho"],  # noqa
    "じゃ": ["ja", "zya", "jya"],
    "じぃ": ["zyi", "jyi"],
    "じゅ": ["ju", "zyu", "jyu"],
    "じぇ": ["je", "zye", "jye"],
    "じょ": ["jo", "zyo", "jyo"],  # noqa
    "すぁ": ["swa"],
    "すぃ": ["swi"],
    "すぅ": ["swu"],
    "すぇ": ["swe"],
    "すぉ": ["swo"],  # noqa
    "ちゃ": ["tya", "cya", "cha"],
    "ちぃ": ["tyi", "cyi"],
    "ちゅ": ["tyu", "cyu", "chu"],
    "ちぇ": ["tye", "cye", "che"],
    "ちょ": ["tyo", "cyo", "cho"],  # noqa
    "ぢゃ": ["dya"],
    "ぢぃ": ["dyi"],
    "ぢゅ": ["dyu"],
    "ぢぇ": ["dye"],
    "ぢょ": ["dyo"],  # noqa
    "つぁ": ["tsa"],
    "つぃ": ["tsi"],
    "つぇ": ["tse"],
    "つぉ": ["tso"],  # noqa
    "てゃ": ["tha"],
    "てぃ": ["thi"],
    "てゅ": ["thu"],
    "てぇ": ["the"],
    "てょ": ["tho"],  # noqa
    "でゃ": ["dha"],
    "でぃ": ["dhi"],
    "でゅ": ["dhu"],
    "でぇ": ["dhe"],
    "でょ": ["dho"],  # noqa
    "とぁ": ["twa"],
    "とぃ": ["twi"],
    "とぅ": ["twu"],
    "とぇ": ["twe"],
    "とぉ": ["two"],  # noqa
    "どぁ": ["dwa"],
    "どぃ": ["dwi"],
    "どぅ": ["dwu"],
    "どぇ": ["dwe"],
    "どぉ": ["dwo"],  # noqa
    "にゃ": ["nya"],
    "にぃ": ["nyi"],
    "にゅ": ["nyu"],
    "にぇ": ["nye"],
    "にょ": ["nyo"],  # noqa
    "ひゃ": ["hya"],
    "ひぃ": ["hyi"],
    "ひゅ": ["hyu"],
    "ひぇ": ["hye"],
    "ひょ": ["hyo"],  # noqa
    "びゃ": ["bya"],
    "びぃ": ["byi"],
    "びゅ": ["byu"],
    "びぇ": ["bye"],
    "びょ": ["byo"],  # noqa
    "ぴゃ": ["pya"],
    "ぴぃ": ["pyi"],
    "ぴゅ": ["pyu"],
    "ぴぇ": ["pye"],
    "ぴょ": ["pyo"],  # noqa
    "ふぁ": ["fa"],
    "ふぃ": ["fi"],
    "ふぅ": ["fu"],
    "ふぇ": ["fe"],
    "ふぉ": ["fo"],
    "ふゃ": ["fya"],
    "ふゅ": ["fyu"],
    "ふょ": ["fyo"],  # noqa
    "ぶぁ": ["bwa"],
    "ぶぃ": ["bwi"],
    "ぶぅ": ["bwu"],
    "ぶぇ": ["bwe"],
    "ぶぉ": ["bwo"],  # noqa
    "ぷぁ": ["pwa"],
    "ぷぃ": ["pwi"],
    "ぷぅ": ["pwu"],
    "ぷぇ": ["pwe"],
    "ぷぉ": ["pwo"],  # noqa
    "みゃ": ["mya"],
    "みぃ": ["myi"],
    "みゅ": ["myu"],
    "みぇ": ["mye"],
    "みょ": ["myo"],  # noqa
    "りゃ": ["rya"],
    "りぃ": ["ryi"],
    "りゅ": ["ryu"],
    "りぇ": ["rye"],
    "りょ": ["ryo"],  # noqa
    # Sokuon 促音
    "っ": [
        None,
        "xtu",
        "xtsu",
        "ltu",
        "ltsu",
    ],  # NOTE: None represents the next character except for "a", "i", "u", "e", "o", "n".  # noqa
}


SMALL_HIRA2ROMA_MAP: dict[str, list[str]] = {
    "ぁ": ["xa", "la"],
    "ぃ": ["xi", "li", "xyi", "lyi"],
    "ぅ": ["xu", "le"],
    "ぇ": ["xe", "le", "xye", "lye"],
    "ぉ": ["xo", "lo"],
    "ゃ": ["xya", "lya"],
    "ゅ": ["xyu", "lyu"],
    "ょ": ["xyo", "lyo"],
    "ゎ": ["lwa", "xwa"],
}


for s_hira, s_romas in SMALL_HIRA2ROMA_MAP.items():
    for k in HIRA2ROMA_MAP.keys():
        if s_hira in k:
            # NOTE: Assume that k is a combination of a single capital hinagana and a single small hiragana  # noqa
            HIRA2ROMA_MAP[k].extend(
                [v1 + v2 for v1, v2 in product(HIRA2ROMA_MAP[k[0]], s_romas) if v1 is not None and v2 is not None]
            )
