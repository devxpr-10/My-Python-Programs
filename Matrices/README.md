# Matrix Library

A lightweight, pure Python implementation of a Matrix class with support for linear algebra operations. Build, manipulate, and perform calculations on matrices with an intuitive API.

## Features

✨ **Core Operations**
- Matrix arithmetic: addition, subtraction, multiplication, and division
- Transpose and determinant computation
- Matrix inverse calculation
- Adjoint and cofactor matrices
- Element-wise access and iteration

🔧 **Utility Functions**
- `identity(n)` - Create n×n identity matrix
- `zeros(rows, cols)` - Create zero matrix
- `ones(rows, cols)` - Create matrix filled with ones

🎯 **Special Methods**
- `minor()` & `minor_mat()` - Compute minors
- `cofactor()` & `cofactor_mat()` - Cofactor calculations
- `adjoint()` - Adjoint matrix
- `get_rows()` & `get_columns()` - Extract rows and columns
- `at(row, col)` - Element access

## Installation

Simply copy `matrix.py` to your project:

```bash
git clone <repository>
cd Matrices
```

## Usage

### Basic Matrix Creation

```python
from matrix import Matrix, identity, zeros, ones

# Create matrix from 2D list
A = Matrix([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

# Create special matrices
I = identity(3)      # 3x3 identity matrix
Z = zeros(2, 4)      # 2x4 zero matrix
O = ones(3, 3)       # 3x3 matrix of ones
```

### Matrix Operations

```python
B = Matrix([[1, 0], [0, 1]])
C = Matrix([[2, 3], [4, 5]])

# Arithmetic operations
result = B + C       # Matrix addition
result = B - C       # Matrix subtraction
result = B * C       # Matrix multiplication
result = B / C       # Matrix division (uses inverse)
result = B * 5       # Scalar multiplication

# In-place operations
B += C
B -= C
B *= C
B /= C
```

### Matrix Properties

```python
A = Matrix([[1, 2], [3, 4]])

# Access matrix properties
print(A.nrows)       # Number of rows
print(A.ncols)       # Number of columns
print(A.order)       # Tuple (rows, cols)
print(A.isSquare)    # Boolean: is matrix square?

# Access elements
element = A[0][1]    # Row 0, Column 1
element = A.at(0, 1) # Same as above
```

### Advanced Operations

```python
A = Matrix([
    [1, 2, 3],
    [0, 1, 4],
    [5, 6, 0]
])

# Determinant and inverse
det = A.det()                 # Determinant of square matrix
A_inv = A.inverse()           # Matrix inverse

# Transpose
A_T = A.transpose()           # Transposed matrix

# Cofactor and adjoint
cofactors = A.cofactor_mat()  # Cofactor matrix
adj = A.adjoint()             # Adjoint matrix

# Extract rows and columns
rows = A.get_rows()           # List of rows
cols = A.get_columns()        # List of columns
```

### Iteration

```python
A = Matrix([[1, 2], [3, 4]])

# Iterate through all elements
for element in A:
    print(element)

# Check membership
if 3 in A:
    print("3 is in the matrix")

# Get total elements
total = len(A)  # Returns nrows * ncols
```

## API Reference

### Constructor

```python
Matrix(data: Sequence[list])
```
Creates a matrix from a 2D sequence. All rows must have the same length.

**Raises:**
- `ValueError` if matrix is empty or rows have different lengths

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `get_rows()` | `list[list]` | Returns list of rows |
| `get_columns()` | `list[list]` | Returns list of columns |
| `transpose()` | `Matrix` | Returns transposed matrix |
| `det()` | `int\|float` | Determinant (square matrices only) |
| `inverse()` | `Matrix` | Matrix inverse |
| `adjoint()` | `Matrix` | Adjoint matrix (square only) |
| `cofactor(row, col)` | `int\|float` | Cofactor at position |
| `cofactor_mat()` | `Matrix` | Cofactor matrix |
| `minor(row, col)` | `int\|float` | Minor at position |
| `minor_mat(row, col)` | `Matrix` | Minor matrix |
| `at(row, col)` | `int\|float` | Element at position |

### Operators

- `+` - Matrix addition
- `-` - Matrix subtraction
- `*` - Matrix multiplication (or scalar)
- `/` - Matrix division (or scalar)
- `+=`, `-=`, `*=`, `/=` - In-place operations
- `[]` - Row access
- `in` - Element membership
- `len()` - Total element count

## Examples

### Solving Linear Systems

```python
# Ax = b, solve for x
A = Matrix([[2, 1], [1, 3]])
b = Matrix([[5], [6]])

# x = A^(-1) * b
x = A.inverse() * b
```

### 2D Transformations

```python
# Rotation matrix
import math
theta = math.pi / 4
rotation = Matrix([
    [math.cos(theta), -math.sin(theta)],
    [math.sin(theta), math.cos(theta)]
])

point = Matrix([[1], [0]])
rotated = rotation * point
```

## Limitations

- Determinant uses cofactor expansion (slow for large matrices)
- Limited to numerical computations
- No built-in matrix decomposition (LU, QR, SVD)
- Singular matrices (det = 0) cannot be inverted

## Contributing

Feel free to fork, improve, and submit pull requests!

## License

MIT License - feel free to use in your projects