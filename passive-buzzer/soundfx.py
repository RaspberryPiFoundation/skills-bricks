"""Sound effects and tunes for a passive buzzer on a Raspberry Pi Pico.

Six effects and four tunes, all played through one passive piezo buzzer
using picozero's Speaker. Call an effect by name, pick one at random with
random_effect(), or play a tune with play_tune().

Wiring matches the Passive buzzer Skill Brick: GP9 to +, the other leg
to GND.
"""

from picozero import Speaker
from random import choice, randint
from time import sleep

# duty_factor 32768 is a 50% duty cycle. The picozero default of 1023 is
# too quiet for the workshop buzzer.
buzzer = Speaker(9, duty_factor=32768)


# --------------------------------------------------------------------
# Sound effects
# --------------------------------------------------------------------

def tada():  # Ta-Daaa!
    buzzer.play(523, 0.1)
    sleep(0.1)
    buzzer.play(523, 0.8)


def chirp():  # series of high-pitched chirps
    for _ in range(2):
        for freq in range(5000, 2999, -100):
            buzzer.play(freq, 0.02)
        sleep(0.2)


def alarm():  # rising tones, over and over
    for _ in range(5):
        for freq in range(2000, 5000, 100):
            buzzer.play(freq, 0.05)
        sleep(0.2)


def siren():  # Nee-Nor!
    for _ in range(10):
        buzzer.play(4500, 0.5)
        buzzer.play(2500, 0.5)


def crash():  # falling whistle, then a crash of white noise
    for freq in range(5000, 1000, -50):
        buzzer.play(freq, 0.05)
    for _ in range(1000):  # one second of noise
        buzzer.play(randint(1000, 5000), 0.001)  # a random pitch each time
    sleep(0.2)


def womp():  # wah-wah-wah-waaaaahhhh
    buzzer.play(494, 0.5)
    buzzer.play(466, 0.5)
    buzzer.play(440, 0.5)
    for _ in range(10):
        buzzer.play(415, 0.05)
        buzzer.play(440, 0.05)
    buzzer.play(415, 0.2)


EFFECTS = [tada, chirp, alarm, siren, crash, womp]


def random_effect():
    """Play one of the six effects, picked at random."""
    choice(EFFECTS)()


# --------------------------------------------------------------------
# Tunes
# --------------------------------------------------------------------
# Note names come from picozero's own note table, which is lower case.
# An empty string is a rest.

TETRIS = ["e5", "g5", "a5", "", "e5", "g5", "b5", "a5", "",
          "e5", "g5", "a5", "", "g5", "e5"]

TWINKLE = ["c4", "c4", "g4", "g4", "a4", "a4", "g4", "",
           "f4", "f4", "e4", "e4", "d4", "d4", "c4"]

IMPERIAL_MARCH = ["a4", "a4", "a4", "f4", "c5", "a4", "f4", "c5", "a5", "",
                  "e5", "e5", "e5", "f5", "c5", "a4", "f4", "c5", "a4"]

NEVER_GONNA = ["a4", "d5", "f#5", "f#5", "e5", "a4", "d5", "e5", "e5",
               "d5", "", "a4", "d5", "d5", "c#4", "a4", "e5", "d5"]

TUNES = {
    "tetris": TETRIS,
    "twinkle": TWINKLE,
    "imperial march": IMPERIAL_MARCH,
    "never gonna": NEVER_GONNA,
}


def play_tune(tune, note_length=0.3):
    """Play a list of note names. Each note lasts note_length seconds."""
    buzzer.play([(note, note_length) for note in tune])


def random_tune():
    """Play one of the four tunes, picked at random."""
    play_tune(choice(list(TUNES.values())))


# --------------------------------------------------------------------

def silence():
    """Stop any sound."""
    buzzer.off()


# Delete the try/finally below once you are calling these from your own
# code. It is here so that running this file on its own makes a noise.
if __name__ == "__main__":
    try:
        siren()
        sleep(0.5)
        play_tune(TETRIS)
        sleep(0.5)
        crash()
    finally:
        silence()
