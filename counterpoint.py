# implementing the counterpoint generator with genetic algorithms
import random
import copy

from fugue import Note
from constants import *
from key_finder import get_key_formatted_from_notes

POPULATION_SIZE = 20  # 20
NUMBER_OF_GENERATIONS = 50  # 50
# mutations
MERGE_RATE = 0.01
DUPLICATION_RATE = 0.005
MUTATION_RATE = 0.05
# other constants, melody-specific
SCALE = []


def get_total_duration(notes: [Note]):
    result = 0
    for note in notes:
        result += note.duration

    return result


def is_in_scale(pitch: int, key: str, is_major: bool):
    degrees = major_degrees if is_major else minor_degrees
    base_scale = {deg + keys_indexes[key] for deg in degrees}
    return (pitch % 12) in base_scale


def generate_random_genome(total_duration: int, key: str, is_major: bool, octave: int):
    # TODO generate empty notes also
    # TODO make optimisation for getting better melodies
    scale = major_degrees if is_major else minor_degrees
    global SCALE
    SCALE = major_degrees if is_major else minor_degrees
    # durations = ['half', 'quarter', 'quarter', 'eighth', 'eighth', 'eighth', 'eighth', 'sixteenth', 'sixteenth', 'sixteenth', 'sixteenth']
    durations = ['half', 'quarter', 'quarter', 'eighth', 'sixteenth']
    notes = []
    last_note = None

    while total_duration != 0:
        if total_duration == 120:
            duration = 'quarter'
        elif total_duration == 480:
            if random.uniform(1, 2) == 1:
                duration = 'half'
            else:
                duration = 'quarter'
        else:
            duration = random.choice(durations)
        while note_duration[duration] > total_duration:
            duration = random.choice(durations)

        degree = random.choice(scale)

        pitch = 12 * octave + keys_indexes[key] + degree
        # to get better melodies by default, if the current note is short, we make it go by step
        if (duration == 'eighth' or duration == 'sixteenth') and last_note is not None:
            sign = random.choice([-1, 1])
            if is_in_scale(last_note.pitch + 1 * sign, key, is_major):
                pitch = last_note.pitch + 1 * sign
            else:
                pitch = last_note.pitch + 2 * sign

        notes.append(Note(pitch, note_duration[duration]))
        last_note = Note(pitch, note_duration[duration])

        total_duration -= note_duration[duration]
    # print(get_total_duration(notes))
    return notes


def generate_random_genome_from_notes(notes):
    key, is_major = get_key_formatted_from_notes(notes)
    total_duration = get_total_duration(notes)
    # will have to decide the octave later
    return generate_random_genome(total_duration, key, is_major, 5)


def mutate(notes):
    # first mutation type, the note merging
    if len(notes) > 1:
        first_note = notes[-1]
        for idx, note in enumerate(notes[:-1:-1]):
            second_note = note
            if random.random() < MERGE_RATE:
                desired_note = random.choice([first_note, second_note])
                notes[idx + 1] = Note(desired_note.pitch, desired_note.duration)
                del notes[idx]

    # second type mutation: the split of notes
    for idx, note in enumerate(notes):
        if random.random() < DUPLICATION_RATE:
            notes.insert(idx + 1, Note(note.pitch, note.duration / 2))
            notes[idx].duration /= 2

    # third mutation, pitch shift
    for note in notes:
        if random.random() < MUTATION_RATE:
            note.pitch += random.choice(SCALE)
    return notes


def crossover(genome1: [Note], genome2: [Note]):
    # split by bars to make sure we don't alter the durations
    bars_nr = get_total_duration(genome1) // note_duration['full']
    if bars_nr > 1:
        split_position = random.randrange(1, bars_nr)
    else:
        split_position = 0
    target_duration_split1 = split_position * note_duration['full']
    target_duration_split2 = split_position * note_duration['full']
    new_genome1 = []
    new_genome2 = []
    saved_notes1 = []
    saved_notes2 = []

    for note1 in genome1:
        if target_duration_split1 >= note1.duration:
            new_genome1.append(note1)
            target_duration_split1 -= note1.duration
        elif target_duration_split1 == 0:
            # the saved notes from first genome will go to the second genome after we process it
            saved_notes1.append(note1)
        elif target_duration_split1 < note1.duration:
            # split note here, to keep the bars integrity
            new_genome1.append(Note(note1.pitch, target_duration_split1))
            saved_notes1.append(Note(note1.pitch, note1.duration - target_duration_split1))
            target_duration_split1 = 0

    for note2 in genome2:
        if target_duration_split2 >= note2.duration:
            new_genome2.append(note2)
            target_duration_split2 -= note2.duration
        elif target_duration_split2 == 0:
            saved_notes2.append(note2)
        elif target_duration_split2 < note2.duration:
            # split note here, to keep the bars integrity
            new_genome2.append(Note(note2.pitch, target_duration_split2))
            saved_notes2.append(Note(note2.pitch, note2.duration - target_duration_split2))
            target_duration_split2 = 0

    new_genome1.extend(saved_notes2)
    new_genome2.extend(saved_notes1)

    return new_genome1, new_genome2


def get_pitches_list(notes1, notes2):
    # returns a list of tuples with pitches played simultaneously
    butchered_notes1 = copy.deepcopy(notes1)
    butchered_notes2 = copy.deepcopy(notes2)

    for i, (note1, note2) in enumerate(zip(butchered_notes1, butchered_notes2)):
        if note1.duration < note2.duration:
            new_note = Note(note2.pitch, note2.duration - note1.duration)
            butchered_notes2.insert(i + 1, new_note)
            note2.duration = note1.duration
        elif note1.duration > note2.duration:
            new_note = Note(note1.pitch, note1.duration - note2.duration)
            butchered_notes1.insert(i + 1, new_note)
            note1.duration = note2.duration

    # print([(x.duration, y.duration) for x, y in zip(butchered_notes1, butchered_notes2)])
    intervals = [(x.pitch, y.pitch, x.duration) for x, y in zip(butchered_notes1, butchered_notes2)]
    return intervals


def fitness(genome: [Note], base_notes: [Note]):
    intervals = get_pitches_list(genome, base_notes)
    last_interval = None
    score = 300

    x, y, duration = intervals[-1]
    if x != 0 and y != 0 and is_consonant_interval[abs(x - y) % 12] is False:
        score -= 40

    for x, y, duration in intervals:
        if x == 0 or y == 0:
            continue
        current_interval = abs(x - y) % 12
        actual_interval = abs(x - y)
        if last_interval is not None:
            # check parallel fifths or octaves/unisons
            if last_interval == current_interval and (current_interval == 0 or current_interval == 7):
                score -= 50
            if is_consonant_interval[last_interval] is False and is_consonant_interval[current_interval] is False and duration >= note_duration['quarter']:
                score -= 10
            if actual_interval == 1 or actual_interval == 2:
                score -= 3
            # if is_consonant_interval[current_interval]

        last_interval = current_interval
    print(score)
    return score


def driver(base_notes):
    population = []
    for i in range(POPULATION_SIZE):
        genome = generate_random_genome_from_notes(base_notes)
        population.append(genome)

    for i in range(NUMBER_OF_GENERATIONS):
        print("****************************************************************************************************")
        print("GENERATION " + str(i))
        last_population = sorted(population, key=lambda g: fitness(g, base_notes), reverse=True)
        population = [last_population[0]]
        elites_count = 1
        if POPULATION_SIZE % 2 is 0:
            population.append(last_population[1])
            elites_count = 2
        for j in range(elites_count, POPULATION_SIZE - 1, 2):
            g1 = last_population[j]
            g2 = last_population[j + 1]
            g1, g2 = crossover(g1, g2)
            g1 = mutate(g1)
            g2 = mutate(g2)
            population.append(g1)
            population.append(g2)

    best_score = -9999
    best_genome = []

    for g in population:
        f = fitness(g, base_notes)
        if f > best_score:
            best_genome = g
            best_score = f

    print("****************************************************************************************************")
    print("RESULT SCORE: " + str(best_score))

    return best_genome
