import random

# Use if you are the wordmaster
game_maker = lambda w: lambda g: len(set([l for l in g if l in w]))

# List of all words
sil = open('wordsEn.txt', 'r')
words = [w for w in sil.read().split() if "'" not in w]

def start_game(num_letters):
    possible_words = list(filter(lambda w: len(w) == num_letters and len(w) ==
    len(set(w)), words))
    guessed_letters = set()
    def update_with_guess(g, num_matches):
        nonlocal possible_words, guessed_letters
        possible_words = list(filter(lambda w: len(set(g).intersection(set(w)))
            == num_matches, possible_words))
        guessed_letters.union(set(g))
        possible_letters = {l for l in alphabet if \
            in_every(possible_words, l)}
        impossible_letters = {l for l in alphabet if \
            not_in_any(possible_words, l)}
        print("Must have {", ''.join(possible_letters), "} and exclude {", \
            ''.join(impossible_letters), "}")
        if len(possible_words) < 8:
            return possible_words
        print("Try guessing " +  random.choice([w for w in possible_words if \
            len(set(w).intersection(guessed_letters)) == 0 or \
            len(set(w).intersection(impossible_letters)) == 0]))
    return update_with_guess

subset_n = lambda lst, n: [[]] if n == 0 else lst and [[lst[0]] + elem for elem
in subset_n(lst[1:], n - 1)] + subset_n(lst[1:], n)

in_every = lambda lst, letter: sum([letter in word for word in lst]) == len(lst)
not_in_any = lambda lst, letter: sum([letter in word for word in lst]) == 0

def best_guess(word_lst, num_letters):
    guess, min_std_dev = '', None
    for word in word_lst:
        remaining = [0] * (num_letters + 1)
        for i in range(num_letters + 1):
            remaining[i] = len(list(filter(lambda w: \
                           len(set(word).intersection(set(w))) == i, \
                           word_lst)))
        new = std_dev(remaining)
        if min_std_dev is None or new < min_std_dev:
            print("Best word to guess is", word)
            min_std_dev, guess = new, word
    print(guess)

def std_dev(lst):
    mean = sum(lst) / len(lst)
    return (sum([(elem - mean)**2 for elem in lst]) / len(lst))**0.5
    
alphabet = set('qwertyuiopasdfghjklzxcvbnm')
