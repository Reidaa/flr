import unittest
from flr.helpers.Qist import Qist


class QistTestCase(unittest.TestCase):
    expected_qist_list = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

    def test_qist_rotation(self):
        qist = Qist(size=20)
        expected = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        for i in range(30):
            qist.append(i)
        self.assertEqual(qist, expected)

    def test_qist_head_access(self):
        qist = Qist(size=20)
        for i in range(30):
            qist.append(i)

        self.assertEqual(qist[0], 29)

    def test_qist_negative_index_1(self):
        qist = Qist(size=20)
        for i in range(30):
            qist.append(i)

        self.assertEqual(qist[-20], 29)


    def test_qist_negative_index_2(self):
        qist = Qist(size=20)
        for i in range(30):
            qist.append(i)

        self.assertEqual(qist[-5], 24)

    def test_qist_negative_index_3(self):
        qist = Qist(size=20)
        for i in range(30):
            qist.append(i)

        self.assertEqual(qist[-1], 28)

    def test_qist_too_big_negative_index(self):
        qist = Qist(size=20)
        for i in range(30):
            qist.append(i)

        with self.assertRaises(IndexError):
            test = qist[-21]

    def test_qist_too_big_positive_index(self):
        qist = Qist(size=20)
        for i in range(30):
            qist.append(i)

        with self.assertRaises(IndexError):
            test = qist[21]

    def test_qist_too_big_positive_index_2(self):
        qist = Qist(size=20)
        for i in range(30):
            qist.append(i)

        with self.assertRaises(IndexError):
            test = qist[20]

    def test_qist_positive_index_1(self):
        qist = Qist(size=20)
        # expected = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        for i in range(30):
            qist.append(i)

        self.assertEqual(qist[1], 10)


    def test_qist_positive_index_2(self):
        qist = Qist(size=20)
        # expected = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        for i in range(30):
            qist.append(i)

        self.assertEqual(qist[5], 14)

    def test_qist_positive_index_3(self):
        qist = Qist(size=20)
        for i in range(30):
            qist.append(i)

        self.assertEqual(qist[20], 29)

    def test_qist_iteration(self):
        qist = Qist(size=20)
        expected = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
        for i in range(30):
            qist.append(i)

        _list = [item for item in qist]

        self.assertEqual(_list, expected)


if __name__ == '__main__':
    unittest.main()
