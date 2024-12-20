# tectonic-solver
repo for the tectonic-solver python solution to be made with Anneroos Christmas 2024

- Step 1: Make it possible to load a Tectonic board  (done)
- Step 2: Create the "Blocks" with their cells (done)
- Step 2b: fill the initial possible-values of the cells per block.
- Step 3: Implement logic - update possible values with multiple logic-rules 
  - -> should always yield in one cell having 1 possible value...
- Step 4: Implement logic - which cell can be placed
- Step 5: Implement solver - (repeated step 3 and step 4)
- Step 6: Make UI - show the logic-rules and cell to be placed of given board
- Step 7: Make UI - to enter / change Tectonic board
- Step 8: Improve input -> convert picture of tectonic into a board
- Step 9: make a website for users to enter/play with tool


Step 1
input two csv-files (board and layout)
1. filled numbers (0 for not-filled)
2. layout (showing which fields belong to which block, identified by number, starting with 0)

Step 2
a Block is collection of 1 or more (up to 5?) Cells -decided to not make a Block-class, as it's "just" a collection
of cells.
a Cell is having a value, a list of possible values based on logic applied, Row, Col (perhaps redundant, but 
good to have for testing) and a list of neighboring Cells
I now have cells-array with all cells, but likely will not be using that, as I also have a blocks-array that shows
the same cells, but grouped per Block.


