from unittest import TestCase
from typing import List

from os import getenv


if not getenv('HYPYXEL_TEST_DEBUG', None):
    def print_debug(*a):
        pass
else:
    def print_debug(*a):
        print(*a)


class HypyxelTestCase(TestCase):

    API_RESPONSE_PROPERTIES = ['raw', 'success', 'error_message']

    RESOURCE_RESPONSE_PROPERTIES = API_RESPONSE_PROPERTIES + ['last_update']

    GUILD_ACHIEVEMENTS_PROPERTIES =\
        RESOURCE_RESPONSE_PROPERTIES + ['one_time', 'tiered']

    class SkipValue:
        pass

    def assert_property_value(self, o: object, p: str, v):
        d = getattr(o, p)

        # Avoid generator issue, get everything to test with value.
        if "generator" in str(type(d)):
            d = tuple(d)

        self.assertTrue(d == v,
                        f'Unexpected value for {p} property ({d} != {v})')

    def check_properties(self, o: object, p: List[str]):
        print_debug(f'Checking properties of: {type(o)}')
        print_debug(f'Properties to check: {p}')

        for i in filter(lambda x: not x.startswith('_'), dir(o)):
            print_debug(f'  Checking for {i} property')
            self.assertTrue(i in p, f'Missing {i} property')
            p.remove(i)

        self.assertTrue(len(p) == 0, f'Extra properties: {p}')

    def check_properties_values(self, o: object, values: dict):

        for k, v in values.items():
            if v is self.SkipValue:
                continue
            self.assert_property_value(o, k, v)

    def properties_full_check(self, o: object, e: dict,
                              base: List[str] = None):
        self.check_properties(o, list(e.keys()) + (base if base else []))
        self.check_properties_values(o, e)
