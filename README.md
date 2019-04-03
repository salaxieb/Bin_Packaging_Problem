## Bin packaging problem 

Solving Bin Packaging problem by Genetic algorithm

### Dependencies:

* python3
* pygame


### Statement:

Task is to cover area of huge rectangle by limited number of smaller rectangles. Below is two examples of good and bad solution.

![screenshot](screenshots/good_solution.png?raw=true)
![screenshot](screenshots/bad_solution.png?raw=true)


### Idea:

Main problem with euristic solution is overlay of boxes one to another. Solution of problem is putting boxes on top of each other. First, gen parameter is flag of turning box to 90 degr., second is level, where you want to put box, third left or right position of box in this level

![screenshot](screenshots/position_choice.png?raw=true)

### Results:

![screenshot](screenshots/results.png?raw=true)

	