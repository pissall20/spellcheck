import re
from collections import Counter

def words(text):
    return re.findall(r'\w+', text.lower())

total_words = Counter(words(open('big.txt').read()))

# Calculate probability of words

def prob(word, n = sum(total_words.values())):
    return total_words[word] / n

# Most probable corrections
def correction(word):
    return max(candidates(word), key=prob)

# Generate possible corrections for the word
def candidates(word):
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

# Subset of words that appear in the dictionary total_words
def known(words):
    return set(w for w in words if w in total_words)

# Calculate edits, one edit away (Insertion, Deletion, Substitution, Transposition)
# All edits that are 1 edit away
def edits1(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word)+1)]
    # Delete the first letter of the index
    deletes = [L + R[1:] for L, R in splits if R]
    # Swap the indexed letter with the next letter in the string
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    # Change one letter to another letter
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    # Insert an extra letter
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


# All edits that are 2 edits away
def edits2(word):
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

# Run correction(wrong) on all (right, wrong) pairs; report results.
def spelltest(tests, verbose=False):
    import time
    start = time.clock()
    good, unknown = 0, 0
    n = len(tests)
    for right, wrong in tests:
        w = correction(wrong)
        good += (w == right)
        if w != right:
            unknown += (right not in total_words)
            if verbose:
                print('correction({}) => {} ({}); expected {} ({})'
                      .format(wrong, w, total_words[w], right, total_words[right]))
    dt = time.clock() - start
    print('{:.0%} of {} correct ({:.0%} unknown) at {:.0f} words per second '
          .format(float(good) / n, n, float(unknown) / n, float(n) / dt))



# Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')] pairs.
def Testset(lines):
    return [(right, wrong)
            for (right, wrongs) in (line.split(':') for line in lines)
            for wrong in wrongs.split()]

spelltest(Testset(open('spell-testset1.txt'))) # Development set
spelltest(Testset(open('spell-testset2.txt'))) # Final test set





