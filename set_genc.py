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


def gen_from_tone_range(tone: int, lowest_spn: str, highest_spn: str):
    if not isinstance(tone, int):
        raise TypeError("tone must be int.")

    lowest_tone = spn2tone(lowest_spn)
    highest_tone = spn2tone(highest_spn)

    distance = calc_dist_from_range(tone, lowest_tone, highest_tone)
    gen = int(distance / 12)
    return gen


def modify_ustx(ustx_filepath, part_name, tone_range):
    if "-" in tone_range:
        lowest, highest = str.split(tone_range, "-", 1)
    else:
        lowest = highest = tone_range

    with open(ustx_filepath, encoding="utf-8") as f:
        ustx = yaml.safe_load(f)

    for part in ustx["voice_parts"]:
        if part["name"] != part_name:
            continue

        curve = {"xs": [], "ys": [], "abbr": "genc"}

        prev_gen = None
        for note in part["notes"]:
            gen = gen_from_tone_range(note["tone"], lowest, highest)
            if gen == prev_gen:
                continue

            curve["xs"] = note["position"]
            curve["ys"] = gen
            prev_gen = gen

        curves = list(filter(lambda curve: curve["abbr"] != "genc", part["curves"]))
        curves.append(curve)
        part["curves"] = curves

    with open(ustx_filepath, mode="w", encoding="utf-8") as f:
        yaml.safe_dump(ustx, f, sort_keys=False)


if __name__ == "__main__":
    args = sys.argv
    modify_ustx(args[1], args[2], args[3])
