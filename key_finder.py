import math
from fugue import Note
from constants import *

"""original KS key profiles"""
#                      C     C#    D     D#     E     F      F#   G     G#    A     A#    B
# major_key_profiles = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
# minor_key_profiles = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]

"""better key profiles (DAVID TEMPERLEY)"""
major_key_profiles = [5, 2, 3.5, 2, 4.5, 4, 2, 4.5, 2, 3.5, 1.5, 4]
minor_key_profiles = [5, 2, 3.5, 4.5, 2, 4, 2, 4.5, 3.5, 2, 1.5, 4]

"""Krumhansl-Schmuckler Key-Finding Algorithm"""


def get_input_vector(notes: [Note]):
    result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for note in notes:
        # 120 because we want to get 0.5 = quarter note duration (just like in the example)
        result[note.pitch % 12] += 60 / note.duration / 2

    return result


def offset_list(lst: [], offset: int):
    return lst[offset:] + lst[:offset]


# gets score for minor and major modes of a scale name by offsetting the key profile vectors
# index is offset from C
# index = 1 means C#
# index = 2 means D etc
def get_score_offset(input_vector, index):
    input_average = sum(input_vector) / len(input_vector)

    major_key_profiles_offset = offset_list(major_key_profiles, index)
    minor_key_profiles_offset = offset_list(minor_key_profiles, index)

    major_key_profiles_average = sum(major_key_profiles_offset) / len(major_key_profiles_offset)
    minor_key_profiles_average = sum(minor_key_profiles_offset) / len(minor_key_profiles_offset)

    # formula in "key for key"
    major_score = sum([(x - input_average) * (y - major_key_profiles_average) for (x, y) in zip(input_vector, major_key_profiles_offset)])
    major_score /= math.sqrt(sum([(x - input_average)**2 for x in input_vector]) * sum([(y - major_key_profiles_average) ** 2 for y in major_key_profiles_offset]))

    minor_score = sum([(x - input_average) * (y - minor_key_profiles_average) for (x, y) in zip(input_vector, minor_key_profiles_offset)])
    minor_score /= math.sqrt(sum([(x - input_average) ** 2 for x in input_vector]) * sum([(y - minor_key_profiles_average) ** 2 for y in minor_key_profiles_offset]))

    return {
        indexes_keys[-index] + ' major': round(major_score, 3),
        indexes_keys[-index] + ' minor': round(minor_score, 3)
    }


def get_score(input_vector):
    score = {}
    for i in range(12):
        score.update(get_score_offset(input_vector, -i))

    return score


def get_key(score):
    max_score = float('-inf')
    key = ''
    for (k, v) in score.items():
        if max_score < v:
            max_score = v
            key = k

    return key
