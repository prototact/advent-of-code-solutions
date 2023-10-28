import unittest as ut
from day19 import rotate_axis


class TestRotations(ut.TestCase):
    def test_rotate_x(self):
        vec = (1, -1, 2)
        other = vec[0], vec[1], vec[2]
        for _ in range(4):
            other = rotate_axis(0, other)
        self.assertEqual(vec, other)
    
    def test_rotate_y(self):
        vec = (1, -1, 2)
        other = vec[0], vec[1], vec[2]
        for _ in range(4):
            other = rotate_axis(1, other)
        self.assertEqual(vec, other)

    def test_rotate_z(self):
        vec = (1, -1, 2)
        other = vec[0], vec[1], vec[2]
        for _ in range(4):
            other = rotate_axis(2, other)
        self.assertEqual(vec, other)


if __name__ == "__main__":
    ut.main()