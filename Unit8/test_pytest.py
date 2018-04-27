#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import pytest


@pytest.fixture
def setup_math():
    import math
    return math


def test_setup_math(setup_math):
    import time
    time.sleep(4)
    assert setup_math.pow(2, 3) == 8.0
