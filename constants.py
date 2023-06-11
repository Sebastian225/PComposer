note_value = {
    'empty': 0,
    'C2': 36,
    'C#2': 37,
    'Db2': 37,
    'D2': 38,
    'D#2': 39,
    'Eb2': 39,
    'E2': 40,
    'F2': 41,
    'F#2': 42,
    'Gb2': 42,
    'G2': 43,
    'G#2': 44,
    'Ab2': 44,
    'A2': 45,
    'A#2': 46,
    'Bb2': 46,
    'B2': 47,
    'C3': 48,
    'C#3': 49,
    'Db3': 49,
    'D3': 50,
    'D#3': 51,
    'Eb3': 51,
    'E3': 52,
    'F3': 53,
    'F#3': 54,
    'Gb3': 54,
    'G3': 55,
    'G#3': 56,
    'Ab3': 56,
    'A3': 57,
    'A#3': 58,
    'Bb3': 58,
    'B3': 59,
    'C4': 60,
    'C#4': 61,
    'Db4': 61,
    'D4': 62,
    'D#4': 63,
    'Eb4': 63,
    'E4': 64,
    'F4': 65,
    'F#4': 66,
    'Gb4': 66,
    'G4': 67,
    'G#4': 68,
    'Ab4': 68,
    'A4': 69,
    'A#4': 70,
    'Bb4': 70,
    'B4': 71,
    'C5': 72,
    'C#5': 73,
    'Db5': 73,
    'D5': 74,
    'D#5': 75,
    'Eb5': 75,
    'E5': 76,
    'F5': 77,
    'F#5': 78,
    'Gb5': 78,
    'G5': 79,
    'G#5': 80,
    'Ab5': 80,
    'A5': 81,
    'A#5': 82,
    'Bb5': 82,
    'B5': 83,
    'C6': 84,
    'C#6': 85,
    'Db6': 85,
    'D6': 86,
    'D#6': 87,
    'Eb6': 87,
    'E6': 88,
    'F6': 89,
    'F#6': 90,
    'Gb6': 90,
    'G6': 91,
    'G#6': 92,
    'Ab6': 92,
    'A6': 93,
    'A#6': 94,
    'Bb6': 94,
    'B6': 95,
    'C7': 96
}

note_duration = {
    'full': 960,
    'full-point': 1440,
    'half': 480,
    'half-point': 720,
    'quarter': 240,
    'quarter-point': 360,
    'eighth': 120,
    'eighth-point': 180,
    'sixteenth': 60,
    'sixteenth-point': 90,
    '32th': 30,
    '32th-point': 45
}

note_duration_names = {
    960: 'full',
    1440: 'full-point',
    480: 'half',
    720: 'half-point',
    240: 'quarter',
    360: 'quarter-point',
    120: 'eighth',
    180: 'eighth-point',
    60: 'sixteenth',
    90: 'sixteenth-point',
    30: '32th',
    45: '32th-point'
}

keys_indexes = {
    'C': 0,
    'C#': 1,
    'D': 2,
    'D#': 3,
    'E': 4,
    'F': 5,
    'F#': 6,
    'G': 7,
    'G#': 8,
    'A': 9,
    'A#': 10,
    'B': 11
}

indexes_keys = [
    'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'
]

major_degrees = [0, 2, 4, 5, 7, 9, 11]

major_degrees_to_index = {
    0: 0,
    2: 1,
    4: 2,
    5: 3,
    7: 4,
    9: 5,
    11: 6
}

minor_degrees = [0, 2, 3, 5, 7, 8, 10]

minor_degrees_to_index = {
    0: 0,
    2: 1,
    3: 2,
    5: 3,
    6: 4,
    7: 4,
    8: 5,
    10: 6
}

is_consonant_interval = {  # true = consonant
    0: True,   # Unison
    1: False,  # Minor second
    2: False,  # Major second
    3: True,  # Minor third
    4: True,   # Major third
    5: False,   # Perfect fourth
    6: False,  # Augmented fourth / Diminished fifth (tritone)
    7: False,   # Perfect fifth # treat fifth as dissonant because invertible counterpoint
    8: True,  # Minor sixth
    9: True,   # Major sixth
    10: False,  # Minor seventh
    11: False,  # Major seventh
    12: True   # Octave
}
