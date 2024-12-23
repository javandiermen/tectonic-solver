# tectonic-solver
repo for the tectonic-solver python solution to be made with Anneroos Christmas 2024

- Step 1: Make it possible to load a Tectonic board  (done)
- Step 2: Create the "Blocks" with their cells (done)
- Step 2b: fill the initial possible-values of the cells per block. (done)
- Step 3: Implement logic - update possible values with multiple logic-rules 
  - -> should always yield in one cell having 1 possible value...
- Step 4: Implement logic - which cell can be placed
- Step 5: Implement solver - (repeated step 3 and step 4)
- Step 6: Make UI - show the logic-rules and cell to be placed of given board (done with matplotlib in tectonic.py)
- Step 7: Make UI - to enter / change Tectonic board (1st playable version using tkinit - run tectonic_tki.py)
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

Step 3
possibilities in cell
added neighbours to cell
made place/remove_domain-functions to be able to "play" programmaticaly

Step 6
Made the board and it's possibilities visible using matplotlib. nice for debugging/testing
however we want of course possibility to play, we need to have interactive-board

Step 7
Made an interactive board using tkinit-library. NB there is an  issue, visible when doing the huge size board, after 
couple of values entered, it is updating the smaller-numbers outside of window.
The smaller-numbers are also bit weird: they are refreshed all the time... due to fact that background-color changes
of the selected cell programmatically we have to update  the possibilities. NB. this is handy for when a value is entered
and possibilities are changing. However somehow if text-string is becoming less, a portion of the previous text is still 
visible (hence I added a couple of extra spaces to de "showpos" function)



