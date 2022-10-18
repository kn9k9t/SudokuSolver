import pathlib
from random import random


class SudokuSolver:
    def generate_new_full_puzzle(self, puzzle):
        free_pos = self.find_first_empty_pos(puzzle)
        if not free_pos:
            return puzzle

        possible_values = self.find_possible_values(puzzle, free_pos)
        if not possible_values:
            return

        next_puzzle = []
        for value in self.randomize_array(possible_values):
            puzzle[free_pos[0]][free_pos[1]] = value
            next_puzzle = self.generate_new_full_puzzle(puzzle)
            if not next_puzzle:
                puzzle[free_pos[0]][free_pos[1]] = '-'
                continue
            elif puzzle == next_puzzle:
                return puzzle
            else:
                puzzle = next_puzzle

        if not next_puzzle:
            return

    def unsolve_full_puzzle(self, puzzle):
        unsolved_puzzle = []
        for row in puzzle:
            unsolved_row = []
            for value in row:
                if random() < 0.5:
                    unsolved_row.append('-')
                else:
                    unsolved_row.append(value)
            unsolved_puzzle.append(unsolved_row)

        return unsolved_puzzle

    def get_random_position(self, len_arr):
        if not len_arr:
            return

        rand_val = random()
        return int(rand_val * (len_arr - 1))

    def randomize_array(self, arr):
        arr= list(arr)
        rand_arr = list()
        step_arr = list(arr)
        for value in step_arr:
            rand_pos = self.get_random_position(len(arr))
            rand_arr.append(arr[rand_pos])
            arr.pop(rand_pos)

        return set(rand_arr)

    def create_empty_puzzle(self):
        puzzle = []
        for i in range(0, 9):
            row = []
            for j in range(0, 9):
                row.append("-")
            puzzle.append(row)

        return puzzle

# ------------------------------------------------------------------------
    def solve_puzzle(self, puzzle):
        free_pos = self.find_first_empty_pos(puzzle)
        if not free_pos:
            return puzzle

        possible_values = self.find_possible_values(puzzle, free_pos)
        if not possible_values:
            return

        next_puzzle = []
        for value in possible_values:
            puzzle[free_pos[0]][free_pos[1]] = value
            next_puzzle = self.solve_puzzle(puzzle)
            if not next_puzzle:
                puzzle[free_pos[0]][free_pos[1]] = '-'
                continue
            elif puzzle == next_puzzle:
                return puzzle
            else:
                puzzle = next_puzzle

        if not next_puzzle:
            return

# ------------------------------------------------------------------------
    def display(self, puzzle):
        table = f""
        rows_count = 0
        for line in puzzle:
            if rows_count == 3:
                table += "---------+---------+---------\n"
                rows_count = 0

            char_count = 0
            for c in line:
                if char_count == 3:
                    table += '|'
                    char_count = 0

                table += f' {c} '
                char_count += 1

            table += "\n"
            rows_count += 1

        print(table)

# ------------------------------------------------------------------------
    def find_possible_values(self, puzzle, pos):
        used_values = set()
        possible_values = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}

        for value in self.get_line(puzzle, pos):
            if value != '-':
                used_values.add(value)
        for value in self.get_column(puzzle, pos):
            if value != '-':
                used_values.add(value)
        for value in self.get_block(puzzle, pos):
            if value != '-':
                used_values.add(value)

        return possible_values.difference(used_values)

    def find_first_empty_pos(self, puzzle):
        line = 0
        column = 0
        for row in puzzle:
            if '-' not in row:
                line += 1
                continue
            for value in row:
                if value == '-':
                    return tuple([line, column])
                column += 1
            line += 1
        return

# ------------------------------------------------------------------------
    def get_line(self, puzzle, pos):
        return puzzle[pos[0]]

    def get_column(self, puzzle, pos):
        column_values = []
        for row in puzzle:
            column_values.append(row[pos[1]])
        return column_values

    def get_block(self, puzzle, pos):
        block_start_line = int(pos[0] / 3) * 3
        block_start_column = int(pos[1] / 3) * 3
        block_values = []
        for row in puzzle[block_start_line:block_start_line + 3]:
            block_values.extend(row[block_start_column:block_start_column + 3])
        return block_values

    def group(self, args, groups_count):
        group = []
        subgroup = []
        for i in range(0, len(args)):
            if len(subgroup) < groups_count:
                subgroup.append(args[i])
            else:
                group.append(subgroup)
                subgroup = []
                subgroup.append(args[i])
        group.append(subgroup)
        return group

    def create_grid(self, puzzle):
        digits = [digit for digit in puzzle if digit in '123456789-']
        return self.group(digits, 9)

# ------------------------------------------------------------------------
    def read_puzzle(self, path_to_puzzle):
        path = pathlib.Path(path_to_puzzle)
        with path.open() as f:
            puzzle = f.read()
        return self.create_grid(puzzle)

    def write_puzzle(self, puzzle):
        file_name = ''
        lines = []
        for row in puzzle:
            line = ''
            for value in row:
                if len(file_name) < 9:
                    if value != '-':
                        file_name += value
                line += value

            lines.append(line + '\n')

        file = open(file_name + '.txt', "x")
        file.writelines(lines)
        file.close()


def main():
    solver = SudokuSolver()
    # empty_puzzle = solver.create_empty_puzzle()
    # new_puzzle = solver.generate_new_full_puzzle(empty_puzzle)
    # new_puzzle = solver.unsolve_full_puzzle(new_puzzle)
    # solver.display(new_puzzle)
    # solver.write_puzzle(new_puzzle)
    # return
    puzzle = solver.read_puzzle("259379372.txt")
    solver.display(puzzle)
    print('#############################\n')
    puzzle = solver.solve_puzzle(puzzle)
    solver.display(puzzle)


if __name__ == '__main__':
    main()
