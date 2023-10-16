import re


def spn2tone(spn):
    tonenames = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")

    matches = re.findall(r"^([a-g]|[cdfga]#)(-1|[0-9])$", spn, flags=re.I)
    if not matches:
        raise ValueError("Invalid (or unsupported) SPN.")

    tonename, octave = matches[0]

    tone = tonenames.index(str.upper(tonename)) + 12 * (int(octave) + 1)
    return tone
