# Gale-Shapley-Algorithm 



Implementation of a popular stable-matching algorithm which produces an array containing a matching between two input sets. Program runs in O(H + S + P) time, where H is the number of hospitals, S the number of students and P the total length of all preference lists. Student rankings are stored in per-student dictionaries and hospitals walk their preference lists with a pointer, so every proposal is resolved in constant time. Sample input and solution files are included. Run the tests with `python3 -m unittest`.

The extensions of the
basic version of the problem are:
1. Each hospital can have any number of positions, not necessarily all the same.
2. A hospital can find some students unacceptable, and a student can find some
hospitals unacceptable.
3. There can be an unequal number of available positions and students.


SAMPLE INPUT STRUCTURE:

num_hospitals num_students

num_positions_0 num_positions_1 ...

hospital 0 preferences

hospital 1 preferences

hospital 1 preferences

.
.
.
student 0 preferences

student 1 preferences

student 1 preferences





----
In Colaboration with [@benberube](https://github.com/bberube2000)
