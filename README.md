#Sudoku Solver

I like playing sudoku so I figured I'd try programming it.

##The Idea
The program uses a min-heap to organize the boxes by the number of possible
answers.  Boxes with only one possible answer, singletons, are popped off the
min-heap and used to simplify the remaining boxes.  If all singletons are
removed and there are still unsolved boxes, uses a depth-first search to find
the answer.

##To-Do
Try and work in other simplifications besides singleton propagation.  For
example, two boxes with two identical numbers as their only possible answers.
