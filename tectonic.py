import csv
#import matplotlib.pyplot as plt
from itertools import combinations


class Cell:
    def __init__(self, row, col, value, block, neighbours, possibilities):
        self.row = row
        self.col = col
        self.value = value
        self.block = block
        self.neighbours = neighbours
        self.possibilities = possibilities

    def __repr__(self):
        return f"Cell(row={self.row}, col={self.col}, value={self.value}, block={self.block}, neighbours={len(self.neighbours)}, possibilities={self.possibilities})"

    def __str__(self):
        return f"Cell(row={self.row}, col={self.col}, value={self.value}, block={self.block}, neighbours={len(self.neighbours)}, possibilities={self.possibilities})"

    def show_pos(self):
        return str(self.possibilities)

def _read_csv(file_path):
    matrix = []
    with open(file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            matrix.append([int(cell) if cell else 0 for cell in row])
    return matrix


class Tectonic:
    def __init__(self):
        self.board = []
        self.layout = []
        self.cells = []
        self.blocks = []
        self.rows=0
        self.cols=0

    def read_from_csv(self, board_file, layout_file):
        self.board = _read_csv(board_file)
        self.rows= len(self.board)
        self.cols= len(self.board[0])
        self.layout = _read_csv(layout_file)
        self.matrix_to_cells()
        self.set_cell_possibilities()
        for cell in self.cells:
            self.set_cell_neighbours(cell)
        for cell in self.cells:
            self.update_block_and_neighbours_possibilities(cell)

    def __str__(self):
        board_str = '\n'.join([' '.join(map(str, row)) for row in self.board])
        layout_str = '\n'.join([' '.join(map(str, row)) for row in self.layout])
        cells_str = '\n'.join(str(cell) for cell in self.cells)
        blocks_str = '\n'.join(
            f"Block {block_num}:\n" + '\n'.join(f"  {cell}" for cell in block)
            for block_num, block in enumerate(self.blocks)
        )
        return f"Board:\n{board_str}\n\nLayout:\n{layout_str}\n\n{cells_str}\n\n{blocks_str}"

    def matrix_to_cells(self):
        max_block_num = max(max(row) for row in self.layout)  # determines the amount of blocks defined in layout
        self.blocks = [[] for _ in range(max_block_num + 1)]  # creates "empty" blocks
        self.cells = []
        for row_idx, row in enumerate(self.board):
            for col_idx, value in enumerate(row):
                block_num = self.layout[row_idx][col_idx]
                cell = Cell(row_idx, col_idx, value, block_num, neighbours=set(), possibilities=set())
                self.cells.append(cell)
                self.blocks[block_num].append(cell)

    def find_cell(self,row,col):
        i=row*len(self.board[0])+col
        # self.cells[i] should be the one..
        if (self.cells[i].row != row or self.cells[i].col !=col):
            print("strange: should be same row/col")
        return self.cells[i]

    def place(self, row, col, value):
        cell=self.find_cell(row,col)
        self.place_cell(cell,value)

    def place_cell(self, cell, value):
        if self.board[cell.row][cell.col] != 0:
            print(f"This is weird: board already containing value:self.board[row][col]")
            exit(1)
        else:
            self.board[cell.row][cell.col] = value
            cell.value=value
            cell.possibilities=set()
            self.update_block_and_neighbours_possibilities(cell)

    # def show_tectonic(self):
    #     # Create a plot
    #     fig,ax = plt.subplots()
    #
    #     # Hide the axes
    #     ax.axis('off')
    #
    #     # Set the limits and aspect ratio
    #     ax.set_xlim(-0.5, len(self.board[0])+0.5)
    #     ax.set_ylim( len(self.board) +0.5 , -0.5)
    #     ax.set_aspect('equal')
    #
    #     xlen=len(self.board[0])+1
    #     ylen=len(self.board) + 1
    #
    #     # Display the matrix values in the cells
    #     for row_idx, row in enumerate(self.board):
    #         for col_idx, value in enumerate(row):
    #             cell=self.cells[row_idx*len(self.board[0])+col_idx]
    #             if self.board[row_idx][col_idx]>0:
    #                 ax.text(col_idx+0.5, row_idx+0.5, self.board[row_idx][col_idx], ha='center', va='center', fontsize=20)
    #             else:
    #                 ax.text(col_idx+0.5, row_idx +0.5 - 0.4, cell.possibilities, ha='center', va='top', fontsize=8)
    #             # Draw vertical gridline (thick border)
    #             ax.axvline(col_idx, ymin=(0.5 / ylen), ymax=((ylen - 0.5) / ylen), color='black', linewidth= 1 if col_idx != 0 else 4)
    #         #draw horizontal gridline (thick border)
    #         ax.axhline(row_idx, xmin=(0.5 / xlen), xmax=((xlen - 0.5) / xlen), color='black', linewidth=1 if row_idx != 0 else 4)
    #     ax.axvline(len(self.board[0]), ymin=(0.5 / ylen), ymax=((ylen - 0.5) / ylen), color='black', linewidth=4)
    #     ax.axhline(len(self.board) , xmin=(0.5 / xlen), xmax=((xlen - 0.5) / xlen), color='black', linewidth=4)
    #
    #
    #
    #     #draw the tectonic borders vertical
    #     for row_idx in range (0,len(self.board)):
    #         for col_idx in range(1, len (self.board[0])):
    #             if self.layout[row_idx][col_idx-1] != self.layout[row_idx][col_idx]:
    #             #     print(f"debug: {row_idx},{col_idx}: ymin={(ylen-(0.5+row_idx))}, ymax={(ylen-(0.5+row_idx+1))}")
    #                 ax.axvline(col_idx, ymin=( (ylen-(0.5+row_idx)) / ylen), ymax=( (ylen-(0.5+row_idx+1)) / ylen), color='black',
    #                            linewidth=4)
    #
    #     #draw the tectonic borders horizontal
    #     for row_idx in range (1,len(self.board)):
    #         for col_idx in range(0, len (self.board[0])):
    #             if self.layout[row_idx-1][col_idx] != self.layout[row_idx][col_idx]:
    #                 # print(f"debug: {row_idx},{col_idx}: xmin={(0.5+col_idx)}, ymax={(0.5+col_idx+1)}")
    #                 ax.axhline(row_idx, xmin=( (0.5+col_idx) / xlen), xmax=( (0.5+col_idx+1) / xlen), color='black',
    #                            linewidth=4)
    #
    #
    #     # Show the plot
    #     width=9
    #     height=9
    #     fig.set_figwidth(width)
    #     fig.set_figheight(height)
    #     plt.show()

    def set_cell_possibilities(self):
        for cell in self.cells:
            if cell.value == 0:
                block_num = cell.block
                possibilities = cell.possibilities
                block = self.blocks[block_num]
                for i in range(1,len(block)+1):
                    possibilities.add(i)

    def set_cell_neighbours(self,cell):
        for other_cell in self.cells:
            if other_cell != cell:
                # print(f"checking: [{cell.row},{cell.col}]-[{other_cell.row},{other_cell.col}]")
                if abs(other_cell.row-cell.row) <= 1 and abs(other_cell.col-cell.col) <= 1:
                    # print(f"adding: [{other_cell.row},{other_cell.col}]")
                    cell.neighbours.add(other_cell)

    def update_block_and_neighbours_possibilities(self,cell):
        # print(f"update_block_and_neighbours_possible : cell:{cell} ")
        if cell.value != 0:
            block = self.blocks[cell.block]
            for block_mate in block:
                #print("block_mate:",block_mate)
                if block_mate != cell:
                    block_mate.possibilities.discard(cell.value)
                    #print("updated block_mate:", block_mate)
            for neighbour in cell.neighbours:
                #print("neighbour:",neighbour)
                neighbour.possibilities.discard(cell.value)
                #print("updated neighbour:", neighbour)

    def remove_cell_domain_x(self,cell:Cell, arvalue):
        for i in arvalue:
            cell.possibilities.discard(i)

    def remove_domain_x(self,row,col, arvalue):
        cell=self.find_cell(row,col)
        for i in arvalue:
            cell.possibilities.discard(i)

    def remove_cell_domain(self,cell:Cell, value):
        cell.possibilities.discard(value)

    def remove_domain(self,row,col, value):
        cell=self.find_cell(row,col)
        cell.possibilities.discard(value)

    def board_filled(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c]==0:
                    return False
        return True

    def find_unique_cell(self, cells):
        # Create a dictionary to count occurrences of each value
        value_count = {}

        # Count occurrences of each value in all sets
        for cell in cells:
            for value in cell.possibilities:
                if value in value_count:
                    value_count[value] += 1
                else:
                    value_count[value] = 1

        # Find the cell with a unique value
        for cell in cells:
            for value in cell.possibilities:
                if value_count[value] == 1:
                    return cell, value

        # If no unique cell is found, return None
        return None, None

    def find_double_cell(self, cells):
        # Create a dictionary to count occurrences of each value
        value_count = {}

        # Count occurrences of each value in all sets
        for cell in cells:
            for value in cell.possibilities:
                if value in value_count:
                    value_count[value] += 1
                else:
                    value_count[value] = 1


        double_cells=[]
        # Find the cells with a double value
        for value in value_count:
            if value_count[value] == 2:
                for cell in cells:
                    for cell2 in cells:
                        if not cell==cell2 and value in cell.possibilities and value in cell2.possibilities:
                            double_cells.append([ cell, cell2, value ])
                            break

        return double_cells



    def check_shared_neighbours_overlapping (self,c: Cell, c2: Cell):
        for v in c.possibilities:
            for n in c.neighbours:
                for n2 in c2.neighbours:
                    if n==n2 and v in n.possibilities:
                        return n, v
        return None, None

    def check_block_shared_neighbours_overlapping_value(self, c:Cell, c2:Cell, v):
        for n in c.neighbours:
            for n2 in c2.neighbours:
                if n == n2 and v in n.possibilities:
                    return n, v
        return None, None

    def check_shared_3_neighbours_overlapping (self,c: Cell, c2: Cell, c3 : Cell):
        for v in c.possibilities:
            for n in c.neighbours:
                for n2 in c2.neighbours:
                    for n3 in c3.neighbours:
                        if n==n2 and n2==n3 and v in n.possibilities:
                            # validate if the found shared neighbour is not one of the three
                            if not n==c2 and not n==c3:
                                return n, v
        return None, None

    def check_shared_3_neighbours_domain (self,c: Cell, c2: Cell, c3 : Cell, remaining_cell: Cell):
        for n in c.neighbours:
            for n2 in c2.neighbours:
                for n3 in c3.neighbours:
                    if n==n2 and n2==n3:                             # validate if the found shared neighbour is not one of the three
                        if not n==c2 and not n==c3 and n.value==0:  #and not n.block==c.block
                            #we've found another cell neigbouring all. if domain of that cell < overlapping domain
                            neighbourhood_domain =c.possibilities.union(c2.possibilities).union(c3.possibilities)
                            friend_domain=n.possibilities
                            potential_remove=neighbourhood_domain.difference(friend_domain)
                            print (f"check_shared_3_neighbours_domain: remaining_cell: ({remaining_cell.row},{remaining_cell.col}) "
                                   f"n-domain={neighbourhood_domain}, f-domain={friend_domain}, len f-n:{len(friend_domain.difference(neighbourhood_domain))}, len n-f:{len(potential_remove)}")
                            if len(friend_domain.difference(neighbourhood_domain))==0:
                                if len(potential_remove)>=1:
                                    #only if other cell has value in domain
                                    for p in potential_remove:
                                        print (f"check if {p} in domain remaining cell")
                                        if p in remaining_cell.possibilities:
                                            print (f"remove {p} from domain")
                                            return n, p
        return None, None

    def check_shared_4_neighbours_domain (self,c: Cell, c2: Cell, c3 : Cell, c4: Cell, remaining_cell: Cell):
        for n in c.neighbours:
            for n2 in c2.neighbours:
                for n3 in c3.neighbours:
                    for n4 in c4.neighbours:
                        if n==n2 and n2==n3 and n3==n4:                             # validate if the found shared neighbour is not one of the three
                            if n not in [c2,c3,c4] and n.value==0:  #and not n.block==c.block
                                #we've found another cell neigbouring all. if domain of that cell < overlapping domain
                                neighbourhood_domain =c.possibilities.union(c2.possibilities).union(c3.possibilities)
                                friend_domain=n.possibilities
                                potential_remove=neighbourhood_domain.difference(friend_domain)
                                print (f"check_shared_4_neighbours_domain: remaining_cell: ({remaining_cell.row},{remaining_cell.col}) "
                                       f"n-domain={neighbourhood_domain}, f-domain={friend_domain}, len f-n:{len(friend_domain.difference(neighbourhood_domain))}, len n-f:{len(potential_remove)}")
                                if len(friend_domain.difference(neighbourhood_domain))==0:
                                    if len(potential_remove)>=1:
                                        #only if other cell has value in domain
                                        for p in potential_remove:
                                            print (f"check if {p} in domain remaining cell")
                                            if p in remaining_cell.possibilities:
                                                print (f"remove {p} from domain")
                                                return n, p
        return None, None


    def check_shared_2_neighbours_domain(self, c: Cell, c2: Cell, remaining_cell: Cell):
        for n in c.neighbours:
            for n2 in c2.neighbours:
                if n == n2 :  # validate if the found shared neighbour is not one of the three
                    if not n == c2:
                        if len(n.possibilities)==2: #for three it can't become empty with 2 neighbours
                            # we've found another cell neigbouring all. if domain of that cell < overlapping domain
                            neighbourhood_domain = c.possibilities.union(c2.possibilities)
                            friend_domain = n.possibilities
                            potential_remove = neighbourhood_domain.difference(friend_domain)
                            if len(friend_domain.difference(neighbourhood_domain)) == 0:
                                if len(potential_remove) == 1:
                                    # only if other cell has value in domain
                                    if next(iter(potential_remove)) in remaining_cell.possibilities:
                                        return n, next(iter(neighbourhood_domain.difference(friend_domain)))
        return None, None

    def differentvalue(self, c1:Cell, c2:Cell):
        #check if these two cells (not neigbours) have connections with other cells in such away we can conclude these are different
        colorlist=[] #start with first cell - find a path until you reach c2 if so: if size of colorlist is even -> True
        current_cell=c1
        colorlist.append(c1)
        same_domain_block=[cell for cell in self.blocks[current_cell.block] if not cell in colorlist and cell.possibilities==current_cell.possibilities ]
        same_domain_neighbour=[cell for cell in current_cell.neighbours if cell.possibilities==current_cell.possibilities]
        same_domain=same_domain_block + [cell for cell in same_domain_neighbour if cell not in same_domain_block]
        if not same_domain:
            return False
        #same domain-cell (s) found
        print (f"Same Domain-cell found: {same_domain}")

        if len(same_domain) > 1:
            print(f"OOPS: multiple found: not yet implemented... {same_domain}")
            return False

        current_cell=same_domain[0]
        colorlist.append(current_cell)
        while not current_cell==c2:
            same_domain_block = [cell for cell in self.blocks[current_cell.block] if
                                    not cell in colorlist and cell.possibilities == current_cell.possibilities]
            same_domain_neighbour = [cell for cell in current_cell.neighbours if
                                    not cell in colorlist and cell.possibilities == current_cell.possibilities]
            same_domain = same_domain_block + [cell for cell in same_domain_neighbour if
                                               cell not in same_domain_block]
            if not same_domain:
                break
            if len(same_domain)>1:
                print (f"OOPS2: multiple found: not yet implemented...{same_domain}")
                return False
            print(f"More same Domain-cell found: {same_domain}")
            current_cell=same_domain[0]
            colorlist.append(current_cell)

        print (f" {len(colorlist)}-{colorlist} ")
        if len(colorlist)%2==0:
            return True

        return False

    def hint(self):
        # give a hint based on current state of board

        # naked single
        for c in self.cells:
            if c.value==0 and len(c.possibilities)==1:
                return  "naked single", "place", c.row, c.col,  next(iter(c.possibilities))
        #hidden single
        for b in self.blocks:
            unique_cell, unique_value = self.find_unique_cell(b)
            if unique_cell:
                return "hidden single", "place", unique_cell.row, unique_cell.col, unique_value

        #two cells in block share a value -> shared neigbours do not share that value
        for b in self.blocks:
            double_cells = self.find_double_cell(b)   #can be multiple to be checked
            for (c,c2,value) in double_cells:
                cell, value = self.check_block_shared_neighbours_overlapping_value(c,c2,value)
                if cell:
                    return "block shared neighbours remove value from domain", "domain_remove", cell.row, cell.col, value


        #two neigbours having 2 values -> shared_neighbours do not have those values
        for c in self.cells:
            if len(c.possibilities)==2:
                    for c2 in c.neighbours:
                        if c2.possibilities == c.possibilities:
                            #check if there are neighbours with overlapping values
                            cell,value  = self.check_shared_neighbours_overlapping(c, c2)
                            if cell:
                                return "shared_neighbours remove domain", "domain_remove", cell.row, cell.col, value

        #three in one block having same domain -> shared neighbours do not have those values
        for b in self.blocks:
            empty_cells =  [cell for cell in b if cell.value == 0]
            for c,c2,c3 in combinations(empty_cells,3):
                if len(c.possibilities.union(c2.possibilities).union(c3.possibilities))==3 :
                    # check if there are neighbours with overlapping values
                    cell, value = self.check_shared_3_neighbours_overlapping(c, c2, c3)
                    if cell:
                        return f"shared_3_in block remove domain ({c.row},{c.col})-({c2.row},{c2.col})-({c3.row},{c3.col})", "domain_remove", cell.row, cell.col, value

        #three neigbours (should all be neigbour amongst eachoter) having 3 same values -> shared_neighbours do not have those values
        for c in self.cells:
            if len(c.possibilities)==3:
                    for c2 in c.neighbours:
                        if c2.possibilities == c.possibilities:
                            for c3 in c.neighbours:
                                if not c2 == c3 and c3 in c2.neighbours and c3.possibilities == c.possibilities:
                                    # check if there are neighbours with overlapping values
                                    cell, value = self.check_shared_3_neighbours_overlapping(c, c2, c3)
                                    if cell:
                                        return "shared_3_neighbours remove domain", "domain_remove", cell.row, cell.col, value

        #one outside of neighbours: if in a block there are multiple cells neighbours of a cell with a domain overlapping the multiple cells, the outsider can not contain a value not in that domain (as that will result in empty neighbour)
        for b in self.blocks:
            empty_cells =  [cell for cell in b if cell.value == 0]
            if len(empty_cells)==4: #4 open cells
                for c,c2,c3 in combinations(empty_cells,3):
                    if len(c.possibilities.union(c2.possibilities).union(c3.possibilities))==4 : #if smaller then other rule already applies
                        # check if there is a neighbours with overlapping values
                        remaining_cell = [cell for cell in empty_cells if cell not in [c, c2, c3]][0]
                        print(f"one outside of 3-neighbourhood potential: remaining: ({remaining_cell.row}, {remaining_cell.col})" )
                        cell, value = self.check_shared_3_neighbours_domain(c, c2, c3, remaining_cell)
                        if cell:
                            print(f"one outside 3-neighbourhood ({c.row},{c.col})-({c2.row},{c2.col})-({c3.row},{c3.col}) ({cell.row},{cell.col}) outside cell not value {value}")
                            return f"one outside 3-neighbourhood: ({cell.row},{cell.col}) -> ({remaining_cell.row},{remaining_cell.col}) value: {value} " , "domain_remove", remaining_cell.row, remaining_cell.col, value

        #one outside of neighbours: if in a block there are multiple cells neighbours of a cell with a domain overlapping the multiple cells, the outsider can not contain a value not in that domain (as that will result in empty neighbour)
        for b in self.blocks:
            empty_cells =  [cell for cell in b if cell.value == 0]
            if len(empty_cells)==3: #3 open cells
                for c,c2 in combinations(empty_cells,2):
                    if len(c.possibilities.union(c2.possibilities))==3 : #if smaller then other rule already applies
                        # check if there is a neighbours with overlapping values
                        remaining_cell = [cell for cell in empty_cells if cell not in [c, c2]][0]
                        cell, value = self.check_shared_2_neighbours_domain(c, c2, remaining_cell)
                        if cell:
                            print(f"one outside 2-neighbourhood ({c.row},{c.col})-({c2.row},{c2.col}) ({remaining_cell.row},{remaining_cell.col}) outside cell not value {value}")
                            return f"one outside 2-neighbourhood: ({cell.row},{cell.col}) -> ({remaining_cell.row},{remaining_cell.col}) value: {value} " , "domain_remove", remaining_cell.row, remaining_cell.col, value

        #one outside of neighbours: if in a block there are multiple cells neighbours of a cell with a domain overlapping the multiple cells, the outsider can not contain a value not in that domain (as that will result in empty neighbour)
        for b in self.blocks:
            empty_cells =  [cell for cell in b if cell.value == 0]
            if len(empty_cells)==4: #4 open cells
                for c,c2 in combinations(empty_cells,2):
                    remaining_cells = [cell for cell in empty_cells if cell not in [c, c2]]
                    for remaining_cell in remaining_cells:
                        cell, value = self.check_shared_2_neighbours_domain(c, c2, remaining_cell)
                        if cell:
                            print(f"outside 2-4-neighbourhood ({c.row},{c.col})-({c2.row},{c2.col}) --clean cell: ({remaining_cell.row},{remaining_cell.col} from: {value} otherwise ({cell.row},{cell.col}) domain {cell.possibilities} becomes empty")
                            return f"outside 2-4neighbourhood: (due to outside cell:({cell.row},{cell.col}) -> ({remaining_cell.row},{remaining_cell.col}) can not have value: {value} " , "domain_remove", remaining_cell.row, remaining_cell.col, value

        # one outside of 4 neighbours: if in a block there are multiple cells neighbours of a cell with a domain overlapping the multiple cells, the outsider can not contain a value not in that domain (as that will result in empty neighbour)
            for b in self.blocks:
                empty_cells = [cell for cell in b if cell.value == 0]
                if len(empty_cells) == 5:  # 4 open cells
                    for c, c2, c3, c4  in combinations(empty_cells, 4):
                        if len(c.possibilities.union(c2.possibilities).union(
                                c3.possibilities)) >= 4:  # if smaller then other rule already applies
                            # check if there is a neighbours with overlapping values
                            remaining_cell = [cell for cell in empty_cells if cell not in [c, c2, c3, c4]][0]
                            print(
                                f"one outside of 4-neighbourhood potential: remaining: ({remaining_cell.row}, {remaining_cell.col})")
                            cell, value = self.check_shared_4_neighbours_domain(c, c2, c3, c4, remaining_cell)
                            if cell:
                                print( f"one outside 4-neighbourhood ({c.row},{c.col})-({c2.row},{c2.col})-({c3.row},{c3.col}-({c4.row},{c4.col}) ({cell.row},{cell.col}) outside cell ({remaining_cell.row},{remaining_cell.col}) not value {value}")
                                return f"one outside 4-neighbourhood: ({cell.row},{cell.col}) -> ({remaining_cell.row},{remaining_cell.col}) value: {value} ", "domain_remove", remaining_cell.row, remaining_cell.col, value

        #coloring
        # if there is a cell with 2 neighbours who have same 2-domain, it could be these cells are a "pair" like when they are neighbours:
        # and similar action as "two neigbours having 2 values -> shared_neighbours do not have those values" is applicable
        # collect all neighbours of the 2-domain neighbours and check if they either end up in same block, or being direct neighbours, so we can conclude that both of them are different / or same
        # example:4x5 - level 8 (46)
        for c in self.cells:
            if len(c.possibilities)>=2:
                empty_neighbours_2domain = [cell for cell in c.neighbours if len(cell.possibilities) == 2]
                if len(empty_neighbours_2domain)>=2:
                    #check if there are  matching domains... theoretically it's perhaps possible to have "multiple" ones (1,2), (3,4),(1,2),(3,4) ?
                    for i1, i2 in combinations([i for i in range(len(empty_neighbours_2domain))], 2):
                        if empty_neighbours_2domain[i1].possibilities ==  empty_neighbours_2domain[i2].possibilities:
                            c1 = empty_neighbours_2domain[i1]
                            c2 = empty_neighbours_2domain[i2]
                            print (f"potential coloring-cell found: ({c.row},{c.col}) - domain: {c.possibilities} with [({c1.row},{c1.col}) - domain: {c1.possibilities} and ({c2.row},{c2.col}) - domain: {c2.possibilities}]")
                            if self.differentvalue(c1,c2):
                                print (f"coloring: different ({c1.row},{c1.col})+({c2.row},{c2.col}) - remove domain  {c1.possibilities} ")
                                for p in c1.possibilities:
                                    if p in c.possibilities:
                                        return f"coloring different ({c1.row},{c1.col})+({c2.row},{c2.col}) - remove value {p} ", "domain_remove", c.row, c.col, p

        return "sorry, I also don't know yet...", "nothing", 0, 0, 0

if __name__ == '__main__':
    t = Tectonic()
    t.read_from_csv("tst/t1.board.csv", "tst/t1.layout.csv")
    # print(t)
    t.place(0, 1, 1)   #naked single
    cell=t.find_cell(4,2)
    t.remove_cell_domain_x(cell,[1,2,4])   #neighbor trio
    t.place_cell(cell,5) #naked single
    t.remove_domain(3,0,1)    #neighbor hidden singles 1
    t.remove_domain(3,1,1)
    t.remove_domain_x(4,1,[2,4])   #neighbor duo
    t.place(4,1,1)
    # t.place(3,3,1) #hidden single
    # t.remove_domain_x(2,1,[4,5])   #neighbor duo
    # t.remove_domain_x(2,1,[2,4])   #neighbor duo
    # t.place(2, 1, 1) #naked single
    # t.remove_domain_x(1,3,[4,5])   #neighbor duo
    # t.place(1, 3, 1) #naked single
    # t.remove_domain_x(0,3,[4,5])   #block duo
    # t.place(0, 3, 3) #naked single
    # t.remove_domain_x(2,0,[2,4])   #block duo
    # t.place(2,0, 5) #naked single
    # t.place(1,1, 4) #naked single
    # t.place(1,0, 2) #naked single
    # t.place(1,2, 5) #naked single
    # t.place(2,3, 4) #naked single
    # t.place(3,2, 2) #naked single
    # t.place(3,1, 4) #naked single
    # t.place(4,3, 4) #naked single
    # t.place(3,0, 2) #naked single
    # t.show_tectonic()
    print("Sorry, Nothing to run here (it's quite stable).\n"
          "Still have to think how I can make automated testcases for all knowledge steps... "
          "-although is it really needed?-")
