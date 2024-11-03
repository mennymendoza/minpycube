# Faces
F = 0
R = 1
B = 2
L = 3
U = 4
D = 5

# Colors
COLORS = [
    "\033[31m",
    "\033[33m",
    "\033[35m",
    "\033[37m",
    "\033[34m",
    "\033[32m",
]
RESET_COLOR = "\033[00m"


class RCube:
    def __init__(self) -> None:
        self.reset()
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

    def __rotatef_cc(self, face: int) -> None:
        """Rotate Face Counter-Clockwise"""
        temp1 = self.cube_mat[0][face][0]
        temp2 = self.cube_mat[0][face][1]
        self.cube_mat[0][face][0] = self.cube_mat[0][face][2]
        self.cube_mat[0][face][1] = self.cube_mat[1][face][2]
        self.cube_mat[0][face][2] = self.cube_mat[2][face][2]
        self.cube_mat[1][face][2] = self.cube_mat[2][face][1]
        self.cube_mat[2][face][2] = self.cube_mat[2][face][0]
        self.cube_mat[2][face][1] = self.cube_mat[1][face][0]
        self.cube_mat[2][face][0] = temp1
        self.cube_mat[1][face][0] = temp2

    def __rotatef_c(self, face: int) -> None:
        """Rotate Face Clockwise"""
        temp1 = self.cube_mat[0][face][0]
        temp2 = self.cube_mat[1][face][0]
        self.cube_mat[0][face][0] = self.cube_mat[2][face][0]
        self.cube_mat[1][face][0] = self.cube_mat[2][face][1]
        self.cube_mat[2][face][0] = self.cube_mat[2][face][2]
        self.cube_mat[2][face][1] = self.cube_mat[1][face][2]
        self.cube_mat[2][face][2] = self.cube_mat[0][face][2]
        self.cube_mat[1][face][2] = self.cube_mat[0][face][1]
        self.cube_mat[0][face][2] = temp1
        self.cube_mat[0][face][1] = temp2

    def __left_horiz_rot(self, row: int) -> None:
        """Left Horizontal Rotation"""
        front_row = self.cube_mat[row][F]
        self.cube_mat[row][F] = self.cube_mat[row][R]
        self.cube_mat[row][R] = self.cube_mat[row][B]
        self.cube_mat[row][B] = self.cube_mat[row][L]
        self.cube_mat[row][L] = front_row

    def __right_horiz_rot(self, row: int) -> None:
        """Right Horizontal Rotation"""
        front_row = self.cube_mat[row][F]
        self.cube_mat[row][F] = self.cube_mat[row][L]
        self.cube_mat[row][L] = self.cube_mat[row][B]
        self.cube_mat[row][B] = self.cube_mat[row][R]
        self.cube_mat[row][R] = front_row

    def __up_vert_rot(self, col: int) -> None:
        """Up Vertical Rotation"""
        front_col = [self.cube_mat[i][F][col] for i in range(3)]
        for i in range(3):
            self.cube_mat[i][F][col] = self.cube_mat[i][D][col]
        for i in range(3):
            self.cube_mat[i][D][col] = self.cube_mat[2 - i][B][2 - col]
        for i in range(3):
            self.cube_mat[i][B][2 - col] = self.cube_mat[2 - i][U][col]
        for i in range(3):
            self.cube_mat[i][U][col] = front_col[i]

    def __down_vert_rot(self, col: int) -> None:
        """Down Vertical Rotation"""
        front_col = [self.cube_mat[i][F][col] for i in range(3)]
        for i in range(3):
            self.cube_mat[i][F][col] = self.cube_mat[i][U][col]
        for i in range(3):
            self.cube_mat[i][U][col] = self.cube_mat[2 - i][B][2 - col]
        for i in range(3):
            self.cube_mat[i][B][2 - col] = self.cube_mat[2 - i][D][col]
        for i in range(3):
            self.cube_mat[i][D][col] = front_col[i]

    def __c_vert_rot(self, col: int) -> None:
        """Clockwise Vertical Rotation"""
        right_col = [self.cube_mat[i][R][col] for i in range(3)]
        for i in range(3):
            self.cube_mat[i][R][col] = self.cube_mat[2 - col][U][i]
        for i in range(3):
            self.cube_mat[2 - col][U][i] = self.cube_mat[2 - i][L][2 - col]
        for i in range(3):
            self.cube_mat[i][L][2 - col] = self.cube_mat[col][D][i]
        for i in range(3):
            self.cube_mat[col][D][i] = right_col[2 - i]

    def __cc_vert_rot(self, col: int) -> None:
        """Counter-clockwise Vertical Rotation"""
        right_col = [self.cube_mat[i][R][col] for i in range(3)]
        for i in range(3):
            self.cube_mat[i][R][col] = self.cube_mat[col][D][2 - i]
        for i in range(3):
            self.cube_mat[col][D][i] = self.cube_mat[i][L][2 - col]
        for i in range(3):
            self.cube_mat[i][L][2 - col] = self.cube_mat[2 - col][U][2 - i]
        for i in range(3):
            self.cube_mat[2 - col][U][i] = right_col[i]

    # All Rubik's Cube Operations
    def __op_u(self) -> None:
        self.__rotatef_c(U)
        self.__left_horiz_rot(0)

    def __op_u_reverse(self) -> None:
        self.__rotatef_cc(U)
        self.__right_horiz_rot(0)

    def __op_e(self) -> None:
        self.__right_horiz_rot(1)

    def __op_e_reverse(self) -> None:
        self.__left_horiz_rot(1)

    def __op_d(self) -> None:
        self.__rotatef_c(D)
        self.__right_horiz_rot(2)

    def __op_d_reverse(self) -> None:
        self.__rotatef_cc(D)
        self.__left_horiz_rot(2)

    def __op_r(self) -> None:
        self.__rotatef_c(R)
        self.__up_vert_rot(2)

    def __op_r_reverse(self) -> None:
        self.__rotatef_cc(R)
        self.__down_vert_rot(2)

    def __op_l(self) -> None:
        self.__rotatef_c(L)
        self.__down_vert_rot(0)

    def __op_l_reverse(self) -> None:
        self.__rotatef_cc(L)
        self.__up_vert_rot(0)

    def __op_m(self) -> None:
        self.__down_vert_rot(1)

    def __op_m_reverse(self) -> None:
        self.__up_vert_rot(1)

    def __op_f(self) -> None:
        self.__rotatef_c(F)
        self.__c_vert_rot(0)

    def __op_f_reverse(self) -> None:
        self.__rotatef_cc(F)
        self.__cc_vert_rot(0)

    def __op_b(self) -> None:
        self.__rotatef_c(B)
        self.__cc_vert_rot(2)

    def __op_b_reverse(self) -> None:
        self.__rotatef_cc(B)
        self.__c_vert_rot(2)

    def __op_s(self) -> None:
        self.__c_vert_rot(1)

    def __op_s_reverse(self) -> None:
        self.__cc_vert_rot(1)

    def __print_face(self, face: int) -> None:
        for i in range(3):
            for j in range(3):
                print(
                    COLORS[self.cube_mat[i][face][j]] + str(self.cube_mat[i][face][j]),
                    end=" ",
                )
            print()

    def reset(self) -> None:
        """Reset Rubik's Cube."""
        self.cube_mat = [
            [[F, F, F], [R, R, R], [B, B, B], [L, L, L], [U, U, U], [D, D, D]],
            [[F, F, F], [R, R, R], [B, B, B], [L, L, L], [U, U, U], [D, D, D]],
            [[F, F, F], [R, R, R], [B, B, B], [L, L, L], [U, U, U], [D, D, D]],
        ]

    def calc_fit(self) -> int:
        """
        Return the fitness of the Rubik's Cube.

        :return: Fitness of the Rubik's Cube.
        :rtype: int
        """
        fitness = 0
        for face in range(6):
            dist = [0] * 6
            for i in range(3):
                for j in range(3):
                    dist[self.cube_mat[i][face][j]] += 1
            fitness += max(dist)
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

    def print_colors(self) -> None:
        """Print cube to standard output with ANSI colors."""
        self.__print_face(U)
        for i in range(3):
            for face in [F, R, B, L]:
                for k in range(3):
                    print(
                        COLORS[self.cube_mat[i][face][k]]
                        + str(self.cube_mat[i][face][k]),
                        end=" ",
                    )
            print()
        self.__print_face(D)
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
