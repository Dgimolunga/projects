# -*- coding: utf-8 -*-
from aiogram.utils.helper import Helper, HelperMode, ListItem


class TestStates(Helper):
    mode = HelperMode.snake_case

    TESTS_STATES_0 = ListItem()
    TESTS_STATES_1 = ListItem()
    TESTS_STATES_2 = ListItem()
    TESTS_STATES_3 = ListItem()
    TESTS_STATES_4 = ListItem()
    TESTS_STATES_5 = ListItem()


if __name__ == "__main__":
    print(TestStates.all())
