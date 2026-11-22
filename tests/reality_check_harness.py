"""Backward-compatible entry point for real subprocess regression tests."""
import pathlib
import sys
import unittest

if __name__ == "__main__":
    root = pathlib.Path(__file__).resolve().parent
    suite = unittest.defaultTestLoader.discover(str(root), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
