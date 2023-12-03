## letter-boxed-solver
NYT letter boxed solver that uses backtracking and bitmasking to search short solutions efficiently. Generalized for a given number of sides and number of characters per side.
For use, run `letterboxed.py` in a CLI and instantiate it. You can change the number of sides and characters per side by editing them in the script.

# Solution
For a given list of line-separated words (in this case, `words.txt`), we preprocess them by first filtering only words that can be formed in the letterboxed instance and then generating a bitmask of characters for the set of legal words. Then we backtrack through them. When we find a short solution, we limit the maximum depth of the backtracking to only focusing on finding smaller solutions. The list of solutions is then sorted and displayed on the CLI.

The backtracking is terminated once all the required characters are found (i.e., the bitmask of required characters is 0.) This is more efficient than checking a global array but restricts us to only use distinct characters across all sides of the instance. A check is also added for each word so that we do not use words that do not reduce the bitmask of required characters.

