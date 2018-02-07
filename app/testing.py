import unittest
from unittest import skip

# from app.to_test import add
from app.to_test import Item


class AdditionTest(unittest.TestCase):
    @skip('wip')
    def test_add_properly(self):
        # ARRANGE
        a = 3
        b = 2
        expectation = 5

        # ACT
        # result = add(a, b)

        # ASSERT
        # self.assertEqual(result, expectation)

    @skip('wip')
    def test_item_borrow(self):
        serial = 'EF6111773'
        location = 'RACK 300'
        new_location = 'RACK 302'
        item = Item(serial, location)
        item.borrow(new_location)
        self.assertEqual(item.serial, serial)
        self.assertEqual(item.status, 'Borrowed')
        self.assertEqual(item.location, new_location)

    @skip('wip')
    def test_item_cannot_borrow(self):
        serial = 'EF6111773'
        location = 'RACK 300'
        new_location = 'RACK 302'
        item = Item(serial, location)
        item.borrow(location)
        self.assertEqual(item.serial, serial)
        self.assertEqual(item.status, 'Borrowed')
        item.borrow(new_location)
        self.assertNotEqual(item.location, new_location)

    def test_item_borrow_invalid_location(self):
        serial = 'EF6111773'
        location = 'RACK 300'
        new_location = 'Toalet'
        item = Item(serial, location)
        # item.borrow(new_location)
        self.assertNotEqual(item.location, new_location)



if __name__ == '__main__':
    unittest.main()