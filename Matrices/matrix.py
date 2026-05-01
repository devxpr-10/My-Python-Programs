from __future__ import annotations
from collections.abc import Sequence

def identity(n: int) -> Matrix:
    l = []
    for r in range(n):
        t = []
        for e in range(n):
            t.append(1 if e == r else 0)
        l.append(t)
    return Matrix(l)

def zeros(rows: int, cols: int) -> Matrix:
    return Matrix([
        [0 for _ in range(cols)]
        for _ in range(rows)
    ])

def ones(rows: int, cols: int) -> Matrix:
    return Matrix([
        [1 for _ in range(cols)]
        for _ in range(rows)
    ])

class Matrix:
    def __init__(self, data: Sequence[list]):
        self.data = [list(row) for row in data]
        self.nrows = len(self.data)
        if self.nrows == 0:
            raise ValueError("Matrix cannot be empty")

        lengths = [len(row) for row in self.data]
        if lengths[0] == 0:
            raise ValueError("Matrix rows cannot be empty")
        if not all(element == lengths[0] for element in lengths):
            raise ValueError("Number of columns should be same")
        self.ncols = lengths[0]

        self.order = (self.nrows, self.ncols)
        self.isSquare = self.ncols == self.nrows

    def get_columns(self) -> list[list]:
        """Returns a list of columns present in current matrix"""
        return [list(col) for col in zip(*self.data)]

    def get_rows(self) -> list[list]:
        """Returns a list of rows present in current matrix"""
        return [row[:] for row in self.data]
    
    def minor_mat(self, row, col):
        return Matrix([
            [value for c, value in enumerate(r) if c != col]
            for r_index, r in enumerate(self.data)
            if r_index != row
        ])

    def minor(self, row, col):
        return self.minor_mat(row, col).det()

    def cofactor(self, row, col):
        return (-1) ** (row + col) * self.minor(row, col)
    
    def cofactor_mat(self):
        return Matrix([
            [self.cofactor(i, j) for j in range(self.ncols)] 
            for i in range(self.nrows)
        ])
    
    def adjoint(self):
        if not self.isSquare:
            raise ValueError("Adjoint only exists for square matrix")
        return self.cofactor_mat().transpose()

    def inverse(self):
        det = self.det()
        if det == 0:
            raise ValueError("Inverse not supported for singular matrices (det = 0)")
        if self.order == (1, 1):
            return Matrix([[1/self[0][0]]])
        return self.adjoint() / det

    def det(self):
        if not self.isSquare:
            raise ValueError("Determinant only exists for square matrices")
        match self.nrows:
            case 1:
                return self.data[0][0]
            case 2:
                return (self.data[0][0] * self.data[1][1]- self.data[0][1] * self.data[1][0])
        d = 0
        for col in range(self.ncols):
            d += self.data[0][col] * self.cofactor(0, col)
        return d

    def transpose(self):
        return Matrix(self.get_columns())

    def at(self, row: int, col: int):
        return self.data[row][col]
        
    def _plus(self, other):
        if self.order != other.order:
            raise ValueError("For Addition, order of both matrices must be same")
        return [
            [left + right for left, right in zip(row, otherrow)]
            for row, otherrow in zip(self.data, other.data)
        ]

    def _sub(self, other):
        if self.order != other.order:
            raise ValueError("For Subtraction, order of both matrices must be same")
        return [
            [left - right for left, right in zip(row, otherrow)]
            for row, otherrow in zip(self.data, other.data)
        ]

    def _mul(self, other: Matrix | int | float):
        if isinstance(other, int | float):
            return [
                [e * other for e in row] for row in self.data
            ]
        elif isinstance(other, Matrix):
            if self.ncols != other.nrows:
                raise ValueError("Number of columns in self must be same as the number of rows in other")
            orows, scols = self.get_rows(), other.get_columns()
            res = []
            for row in orows:
                temp = []
                for col in scols:
                    e = sum(se * oe for se, oe in zip(row, col))
                    temp.append(e)
                res.append(temp)
            return res
        else:
            raise TypeError(type(other).__name__, "not supported")
            
    def _div(self, other: Matrix | int | float):
        if isinstance(other, int | float):
            return self._mul(1/other)
        elif isinstance(other, Matrix):
            return self * other.inverse()
        else:
            raise TypeError(type(other).__name__, "not supported")

    def add(self, other):
        """Adds the other matrix into this one."""
        self.data = self._plus(other)
        return self

    def subtract(self, other):
        """Subtracts the other matrix from this one"""
        self.data = self._sub(other)
        return self
    
    def multiply(self, other):
        """Multiplies the other matrix with this one"""
        self.data = self._mul(other)
        self.nrows = len(self.data)
        lengths = [len(row) for row in self.data]
        self.ncols = lengths[0]
        self.order = (self.nrows, self.ncols)

        return self
    
    def divide(self, other):
        """Divides the other matrix with this one"""
        self.data = self._div(other)
        self.nrows = len(self.data)
        lengths = [len(row) for row in self.data]
        self.ncols = lengths[0]
        self.order = (self.nrows, self.ncols)
        return self

    def __add__(self, other): return Matrix(self._plus(other))
    def __sub__(self, other): return Matrix(self._sub(other))
    def __mul__(self, other): return Matrix(self._mul(other))
    def __rmul__(self, other): return Matrix(self._mul(other))
    def __truediv__(self, other): return Matrix(self._div(other))
    def __iadd__(self, other): return self.add(other)
    def __isub__(self, other): return self.subtract(other)
    def __imul__(self, other): return self.multiply(other)
    def __itruediv__(self, other): return self.divide(other)
    def __getitem__(self, key): return self.data[key]
    def __contains__(self, item): return any(item in row for row in self.data)
    def __len__(self): return self.ncols * self.nrows
    # def __pow__(self, other: int | float):
    #     if other == -1:
    #         return self.inverse()
    #     elif other == 0 and self.isSquare:
    #         return identity(self.ncols)
    #     elif other > 0:
    #         ...
    def __iter__(self):
        for row in self.data:
            for e in row:
                yield e
    
    def __eq__(self, value: Matrix):
        if not isinstance(value, Matrix):
            return False
        if self.order != value.order:
            return False
        return all(
            abs(self.data[i][j] - value.data[i][j]) < 1e-9
            for i in range(self.nrows)
            for j in range(self.ncols)
        )

    def __str__(self):
        return "\n".join("  ".join(' ' + str(n) for n in row) for row in self.data)

if __name__ == '__main__':
    mat1 = Matrix([[3, 3],
                  [2, 3],
                  [6, 4]])
    mat2 = Matrix([[2, 1, 4],
                  [53, 24, 5]])
    # mat2.subtract(mat1)
    # print(mat1.inverse())
    # print(0 in mat1)
    # print((mat1*2) == (mat1+mat1))
    print(mat1 ** 2)