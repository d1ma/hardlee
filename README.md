## Usage instructions

        from translator import Translator
        t = Translator()
        pr = t.get_pronounciation('Some english sentence')
        possibilities = t.get_plaintext(pr)
        close_possibilities = t.get_plaintext(pr, .3)

## Todo

- distance metric right now is every close syllable change is penalized by .1. We should extend this to make it cheaper for closer syllables and more expensive for farther ones
- parse the `possibilities` phrase to make sure it's legitimate english phrase, not just a random collection of words
