import os
# so the requirements are to create a list of best letter boxed solutions
# letter boxed be defined as a list of sets called sides
# letter boxed traditionally has 4 sides of 3 letter
num_sides = 4
side_length = 3
max_words_allowed = 6

# instantiating the letter boxed instance
letter_boxed = [set() for _ in range(num_sides)]

for side in range(num_sides):
    print(f'Enter the characters for {side} side: ')
    for letter in range(side_length):
        letter_boxed[side].add(input())

'''
example, for this instance of letterboxed
letter_boxed = [set(['A', 'B', 'X']), set(['Q', 'S', 'O']), set(['D', 'R', 'I']), set(['M', 'U', 'N'])]
best solution is [marquis, sandbox]
'''

# getting the list of all words
with open(os.path.join(os.getcwd(), 'words.txt')) as f:
    words = f.read().splitlines()

# creating a filter of words
# first we must filter the words that do not contain the list of characters in the instance
required_letters = set().union(*letter_boxed)
bitmap_filter = 0
for letter in required_letters:
    bitmap_filter |= (1 << (ord(letter) - ord('A')))

def letter_filter(word : str):
    for letter in word:
        if ord(letter) < ord('A'): 
            return False
        elif (bitmap_filter & (1 << (ord(letter) - ord('A')))) == 0:
            return False
    return True
filtered_words = [word for word in words if letter_filter(word)]

# now these letters must be filtered so that no two consecutive letters belong to the same set
letter_side_map = {}
for (side_num, side) in enumerate(letter_boxed):
    for letter in side:
        letter_side_map[letter] = side_num
def consecutive_letter_filter(word: str):
    for i in range(1, len(word)):
        if letter_side_map[word[i - 1]] == letter_side_map[word[i]]:
            return False
    return True
final_word_list = [word for word in filtered_words if consecutive_letter_filter(word)]
 
# final_word_list contains all the valid words we could have in a list
# since a solution string has the constraint last letter of prev == first_letter of next
# we want to split final_word_list into a list of lists
list_by_character = [[] for _ in range(26)]
for word in final_word_list:
    word_bitmap = 0
    for letter in word:
        word_bitmap |= (1 << (ord(letter) - ord('A')))
    list_by_character[ord(word[0]) - ord('A')].append((word, word_bitmap))

# now we have a backtracking solution on the filtered words
list_of_solutions = []
current_solution = []
def enumerate_solutions(bit_filter : int, curr_start_letter : chr):
    global max_words_allowed

    if len(current_solution) > max_words_allowed:
        return
    if bit_filter == 0:
        # print(current_solution)
        list_of_solutions.append(current_solution.copy())
        max_words_allowed = min(max_words_allowed, len(current_solution) - 1)
        return
    
    words = list_by_character[ord(curr_start_letter) - ord('A')]
    for (word, word_bitmap) in words:
        # we want every bit that is set in word_bitmap to be become 0 in bit_filter
        new_bit_filter = bit_filter & ~(word_bitmap)
        if new_bit_filter < bit_filter:
            current_solution.append(word)
            enumerate_solutions(new_bit_filter, word[len(word) - 1])
            current_solution.pop()
        if len(current_solution) >= max_words_allowed:
            return

for i in range(26):
    enumerate_solutions(bitmap_filter, chr(i + ord('A')))

list_of_solutions.sort(key=len)
print("the best solutions are:")
for i in range(min(10, len(list_of_solutions))):
    print(list_of_solutions[i])

if len(list_of_solutions) != 0:
    print(f'best solution is {list_of_solutions[0]}')
else:
    print('No solution found')

# we also display all solutions less than equal to two words, since those are hardest to find
max_words_allowed = 2
def two_word_solutions(bit_filter : int, curr_start_letter : chr):
    if len(current_solution) > max_words_allowed:
        return
    if bit_filter == 0:
        print(current_solution)
        return
    
    words = list_by_character[ord(curr_start_letter) - ord('A')]
    for (word, word_bitmap) in words:
        # we want every bit that is set in word_bitmap to be become 0 in bit_filter
        new_bit_filter = bit_filter & ~(word_bitmap)
        if(new_bit_filter < bit_filter):
            current_solution.append(word)
            two_word_solutions(new_bit_filter, word[len(word) - 1])
            current_solution.pop()

print('All two word solutions are:')
for i in range(26):
    if(bitmap_filter & (1 << i)):
        two_word_solutions(bitmap_filter, chr(i + ord('A')))




    









