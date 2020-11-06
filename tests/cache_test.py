import unittest
import time

import lucidcache

class TestCorrect(unittest.TestCase):
    def test__init__(self):
        self.a = 0

        self.assertEqual(self.get_a(), 0)
        self.assertIn(self.get_a._func_id, lucidcache.cache.keys())
        self.add_a()
        self.assertEqual(self.get_a(), 1)

    @lucidcache.cacheable
    def get_a(self):
        return self.a

    @lucidcache.nocache(get_a)
    def add_a(self):
        self.a += 1

class TestWrong(unittest.TestCase):
    def test__init__(self):
        self.b = 0

        self.assertEqual(self.get_b(), 0)
        self.assertIn(self.get_b._func_id, lucidcache.cache.keys())
        self.add_b()
        self.assertNotEqual(self.get_b(), self.b)

    @lucidcache.cacheable
    def get_b(self):
        return self.b

    def add_b(self):
        self.b += 1

class TestNoCacheAll(unittest.TestCase):
    def test__init__(self):
        self.c = 0
        self.d = 0

        self.assertEqual(self.get_c(), 0)
        self.assertEqual(self.get_d(), 0)
        self.add_c()
        self.add_d()
        self.assertEqual(self.get_c(), 0)
        self.assertEqual(self.get_d(), 0)
        self.clear()
        self.assertEqual(self.get_c(), 1)
        self.assertEqual(self.get_d(), 1)

    @lucidcache.cacheable
    def get_c(self):
        return self.c

    @lucidcache.cacheable
    def get_d(self):
        return self.d

    def add_c(self):
        self.c += 1

    def add_d(self):
        self.d += 1

    @lucidcache.nocacheall
    def clear(self):
        pass

class TestHeavy(unittest.TestCase):
    def test__init__(self):
        start_time = int(time.time() * 1000)
        self.factorial(50000)
        no_cached_time = int(time.time() * 1000) - start_time

        start_time = int(time.time() * 1000)
        self.factorial(50000)
        cached_time = int(time.time() * 1000) - start_time

        self.assertLess(cached_time, no_cached_time)
        self.assertLess(cached_time, 10)

    @lucidcache.cacheable
    def factorial(self, n):
        factorial = 1
        while n:
            factorial *= n
            n -= 1
        return factorial

class TestRecursion(unittest.TestCase):
    def test__init__(self):
        self.assertEqual(self.factorial(10), 3628800)
        self.assertEqual(self.factorial(10), 3628800)

    @lucidcache.cacheable
    def factorial(self, n):
        if n < 2:
            return 1
        return n * self.factorial(n - 1)

unittest.main()