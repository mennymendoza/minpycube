import math

# Faces
F = 0
R = 1
B = 2
L = 3
U = 4
D = 5

# Column indices
F_START = F * 3
R_START = R * 3
B_START = B * 3
L_START = L * 3
U_START = U * 3
D_START = D * 3

# Colors
COLOR_MAP = {
    F: "\x1b[31m",
    R: "\033[33m",
    B: "\033[35m",
    L: "\033[37m",
    U: "\033[34m",
    D: "\033[32m",
}
RESET_COLOR = "\033[00m"


class RCube:
    def __init__(self):
        self.cube_mat = [
            [F, F, F, R, R, R, B, B, B, L, L, L, U, U, U, D, D, D],
            [F, F, F, R, R, R, B, B, B, L, L, L, U, U, U, D, D, D],
            [F, F, F, R, R, R, B, B, B, L, L, L, U, U, U, D, D, D],
        ]
        self.op_function_map = {
            "U": self.__op_u,
            "-U": self.__op_u_reverse,
            "E": self.__op_e,
            "-E": self.__op_e_reverse,
            "D": self.__op_d,
            "-D": self.__op_d_reverse,
            "R": self.__op_r,
            "-R": self.__op_r_reverse,
            "L": self.__op_l,
            "-L": self.__op_l_reverse,
            "M": self.__op_m,
            "-M": self.__op_m_reverse,
            "F": self.__op_f,
            "-F": self.__op_f_reverse,
            "B": self.__op_b,
            "-B": self.__op_b_reverse,
            "S": self.__op_s,
            "-S": self.__op_s_reverse,
        }

    def __rotatef_cc(self, face):
        """Rotate Face Counter-Clockwise"""
        base = face * 3
        temp1 = self.cube_mat[0][base]
        temp2 = self.cube_mat[0][base + 1]
        self.cube_mat[0][base] = self.cube_mat[0][base + 2]
        self.cube_mat[0][base + 1] = self.cube_mat[1][base + 2]
        self.cube_mat[0][base + 2] = self.cube_mat[2][base + 2]
        self.cube_mat[1][base + 2] = self.cube_mat[2][base + 1]
        self.cube_mat[2][base + 2] = self.cube_mat[2][base]
        self.cube_mat[2][base + 1] = self.cube_mat[1][base]
        self.cube_mat[2][base] = temp1
        self.cube_mat[1][base] = temp2

    def __rotatef_c(self, face):
        """Rotate Face Clockwise"""
        base = face * 3
        temp1 = self.cube_mat[0][base]
        temp2 = self.cube_mat[1][base]
        self.cube_mat[0][base] = self.cube_mat[2][base]
        self.cube_mat[1][base] = self.cube_mat[2][base + 1]
        self.cube_mat[2][base] = self.cube_mat[2][base + 2]
        self.cube_mat[2][base + 1] = self.cube_mat[1][base + 2]
        self.cube_mat[2][base + 2] = self.cube_mat[0][base + 2]
        self.cube_mat[1][base + 2] = self.cube_mat[0][base + 1]
        self.cube_mat[0][base + 2] = temp1
        self.cube_mat[0][base + 1] = temp2

    def __copy_row(self, row, face1, face2):
        """Copy a row from face1 to face2. Rows are numbered from 0 to 2."""
        base1 = face1 * 3
        base2 = face2 * 3
        for i in range(0, 3):
            self.cube_mat[row][base2 + i] = self.cube_mat[row][base1 + i]

    def __left_horiz_rot(self, row):
        """Left Horizontal Rotation"""
        front_row = [
            self.cube_mat[row][0],
            self.cube_mat[row][1],
            self.cube_mat[row][2],
        ]
        self.__copy_row(row, R, F)
        self.__copy_row(row, B, R)
        self.__copy_row(row, L, B)
        for i in range(0, 3):
            self.cube_mat[row][L_START + i] = front_row[i]

    def __right_horiz_rot(self, row):
        """Right Horizontal Rotation"""
        front_row = [
            self.cube_mat[row][0],
            self.cube_mat[row][1],
            self.cube_mat[row][2],
        ]
        self.__copy_row(row, L, F)
        self.__copy_row(row, B, L)
        self.__copy_row(row, R, B)
        for i in range(0, 3):
            self.cube_mat[row][R_START + i] = front_row[i]

    def __up_vert_rot(self, col):
        """Up Vertical Rotation"""
        front_col = [
            self.cube_mat[0][col],
            self.cube_mat[1][col],
            self.cube_mat[2][col],
        ]
        for i in range(0, 3):
            self.cube_mat[i][F_START + col] = self.cube_mat[i][D_START + col]
        for i in range(0, 3):
            self.cube_mat[i][D_START + col] = self.cube_mat[2 - i][B_START + (2 - col)]
        for i in range(0, 3):
            self.cube_mat[i][B_START + (2 - col)] = self.cube_mat[2 - i][U_START + col]
        for i in range(0, 3):
            self.cube_mat[i][U_START + col] = front_col[i]

    def __down_vert_rot(self, col):
        """Down Vertical Rotation"""
        front_col = [
            self.cube_mat[0][col],
            self.cube_mat[1][col],
            self.cube_mat[2][col],
        ]
        for i in range(0, 3):
            self.cube_mat[i][F_START + col] = self.cube_mat[i][U_START + col]
        for i in range(0, 3):
            self.cube_mat[i][U_START + col] = self.cube_mat[2 - i][B_START + (2 - col)]
        for i in range(0, 3):
            self.cube_mat[i][B_START + (2 - col)] = self.cube_mat[2 - i][D_START + col]
        for i in range(0, 3):
            self.cube_mat[i][D_START + col] = front_col[i]

    def __c_vert_rot(self, col):
        """Clockwise Vertical Rotation"""
        right_col = [
            self.cube_mat[0][R_START + col],
            self.cube_mat[1][R_START + col],
            self.cube_mat[2][R_START + col],
        ]
        for i in range(0, 3):
            self.cube_mat[i][R_START + col] = self.cube_mat[2 - col][U_START + i]
        for i in range(0, 3):
            self.cube_mat[2 - col][U_START + i] = self.cube_mat[2 - i][
                L_START + (2 - col)
            ]
        for i in range(0, 3):
            self.cube_mat[i][L_START + (2 - col)] = self.cube_mat[col][D_START + i]
        for i in range(0, 3):
            self.cube_mat[col][D_START + i] = right_col[2 - i]

    def __cc_vert_rot(self, col):
        """Counter-clockwise Vertical Rotation"""
        right_col = [
            self.cube_mat[0][R_START + col],
            self.cube_mat[1][R_START + col],
            self.cube_mat[2][R_START + col],
        ]
        for i in range(0, 3):
            self.cube_mat[i][R_START + col] = self.cube_mat[col][D_START + (2 - i)]
        for i in range(0, 3):
            self.cube_mat[col][D_START + i] = self.cube_mat[i][L_START + (2 - col)]
        for i in range(0, 3):
            self.cube_mat[i][L_START + (2 - col)] = self.cube_mat[2 - col][
                U_START + (2 - i)
            ]
        for i in range(0, 3):
            self.cube_mat[2 - col][U_START + i] = right_col[i]

    # All Rubik's Cube Operations
    def __op_u(self):
        self.__rotatef_c(U)
        self.__left_horiz_rot(0)

    def __op_u_reverse(self):
        self.__rotatef_cc(U)
        self.__right_horiz_rot(0)

    def __op_e(self):
        self.__right_horiz_rot(1)

    def __op_e_reverse(self):
        self.__left_horiz_rot(1)

    def __op_d(self):
        self.__rotatef_c(D)
        self.__right_horiz_rot(2)

    def __op_d_reverse(self):
        self.__rotatef_cc(D)
        self.__left_horiz_rot(2)

    def __op_r(self):
        self.__rotatef_c(R)
        self.__up_vert_rot(2)

    def __op_r_reverse(self):
        self.__rotatef_cc(R)
        self.__down_vert_rot(2)

    def __op_l(self):
        self.__rotatef_c(L)
        self.__down_vert_rot(0)

    def __op_l_reverse(self):
        self.__rotatef_cc(L)
        self.__up_vert_rot(0)

    def __op_m(self):
        self.__down_vert_rot(1)

    def __op_m_reverse(self):
        self.__up_vert_rot(1)

    def __op_f(self):
        self.__rotatef_c(F)
        self.__c_vert_rot(0)

    def __op_f_reverse(self):
        self.__rotatef_cc(F)
        self.__cc_vert_rot(0)

    def __op_b(self):
        self.__rotatef_c(B)
        self.__cc_vert_rot(2)

    def __op_b_reverse(self):
        self.__rotatef_cc(B)
        self.__c_vert_rot(2)

    def __op_s(self):
        self.__c_vert_rot(1)

    def __op_s_reverse(self):
        self.__cc_vert_rot(1)

    def reset(self) -> None:
        """Reset Rubik's Cube."""
        self.cube_mat = [
            [F, F, F, R, R, R, B, B, B, L, L, L, U, U, U, D, D, D],
            [F, F, F, R, R, R, B, B, B, L, L, L, U, U, U, D, D, D],
            [F, F, F, R, R, R, B, B, B, L, L, L, U, U, U, D, D, D],
        ]

    def calc_fit(self) -> int:
        """
        Return the fitness of the Rubik's Cube.

        :return: Fitness of the Rubik's Cube.
        :rtype: int
        """
        fitness = 0
        for i in range(0, 3):
            for j in range(0, 18):
                fitness += int(self.cube_mat[i][j] == math.floor(j / 3))
        return fitness

    def rotate(self, op: str) -> None:
        """
        Perform an operation on the Rubik's Cube.

        :param op: Operation represented as a string in standard move notation.
        :type op: str
        """
        if op not in self.op_function_map:
            print("Invalid operation string.")
            return
        self.op_function_map[op]()

    def run_list(self, op_list: list[str]) -> int:
        """Run a list of operations and return the fitness of the final state.

        :param op_list: List of Rubik's Cube operations, represented as a list of strings in standard move notation.
        :type op_list: list[str]
        :return: Fitness of the Rubik's Cube.
        :rtype: int
        """
        for op in op_list:
            self.rotate(op)
        return self.calc_fit()

    def print_colors(self) -> None:
        """Print cube to standard output with ANSI colors."""
        for i in range(0, 3):
            for j in range(0, 18):
                print(
                    COLOR_MAP[self.cube_mat[i][j]] + str(self.cube_mat[i][j]), end=" "
                )
            print()
        print(RESET_COLOR)

    @staticmethod
    def invert_op(op: str) -> str:
        """
        Return the inverse of the input operation as a string.

        :param op: Operation represented as a string in standard move notation.
        :type op: str
        :return: Inverse of the input operation as a string.
        :rtype: str
        """
        if op.startswith("-"):
            return op.replace("-", "")
        else:
            return "-" + op
