"""Test MultiScaleMNIST generating."""
import numpy as np
import pytest

from multiscalemnist.generate import filled_margin, random_cell, random_coordinate


@pytest.mark.parametrize("min_val, max_val", [(0, 3), (5, 12), (120, 332)])
def test_random_coordinate(min_val, max_val):
    """Test drawing random coordinate."""
    assert min_val <= random_coordinate(min_val, max_val) < max_val


@pytest.mark.parametrize("_iter", range(5))
@pytest.mark.parametrize("grid_size", [[2, 2], [5, 5], [3, 7]])
def test_random_cell(grid_size, _iter):
    """Test drawing random indices in grid."""
    grid = np.zeros(grid_size)
    y_idx, x_idx = random_cell(grid)
    assert 0 <= y_idx < grid_size[0]
    assert 0 <= x_idx < grid_size[1]


@pytest.mark.parametrize("_iter", range(5))
def test_draw_indices_with_ones(_iter):
    """Test if nonzero cell is not drawn."""
    grid = np.zeros((3, 3))
    nonzero_inds = random_cell(grid)
    grid[nonzero_inds] = 1
    inds = random_cell(grid)
    assert not (inds[0] == nonzero_inds[0] and inds[1] == nonzero_inds[1])


def test_draw_indices_ones():
    """Test if None returned when no indices can be drawn."""
    grid = np.ones((3, 3))
    assert random_cell(grid) is None


@pytest.mark.parametrize(
    "nonzero, cell_idx, expected",
    [
        ([], (2, 2), (5, 5)),
        ([(1, 1)], (2, 1), (1, 5)),
        ([(1, 1)], (1, 2), (5, 1)),
        ([(2, 0), (1, 2)], (2, 2), (1, 2)),
    ],
)
def test_filled_margin(nonzero, cell_idx, expected):
    """Test filled margin."""
    grid = np.zeros((5, 5))
    for y_idx, x_idx in nonzero:
        grid[y_idx, x_idx] = 1
    assert filled_margin(grid, cell_idx) == expected
