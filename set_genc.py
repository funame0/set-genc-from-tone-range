import re
import sys
import yaml


def spn2tone(spn):
    tonenames = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")

    matches = re.findall(r"^([a-g]|[cdfga]#)(-1|[0-9])$", spn, flags=re.I)
    if not matches:
        raise ValueError("Invalid (or unsupported) SPN.")

    tonename, octave = matches[0]

    tone = tonenames.index(str.upper(tonename)) + 12 * (int(octave) + 1)
    return tone


def calc_dist_from_range(tone, lowest, highest):
    if tone < lowest:
        return lowest - tone
    if tone > highest:
        return highest - tone
    return 0


def genc_from_tone_range(tone: int, lowest_spn: str, highest_spn: str):
    if not isinstance(tone, int):
        raise TypeError("tone must be int.")

    lowest_tone = spn2tone(lowest_spn)
    highest_tone = spn2tone(highest_spn)

    distance = calc_dist_from_range(tone, lowest_tone, highest_tone)
    genc = int(distance / 12)
    return genc
