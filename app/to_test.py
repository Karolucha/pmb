import re


class Item:
    def __init__(self, serial, location):
        self.serial = serial
        self.status = 'Available'
        self.location = None

        self.set_location(location)

    def borrow(self, where):
        if self.status == 'Available':
            self.status = 'Borrowed'
            self.set_location(where)
        else:
            print('Already borrowed!')

    def return_item(self, to):
        self.status = 'Available'
        self.set_location(to)

    def set_location(self, value):
        print('set locatiob')
        if re.search('RACK\s\d+', value):
            print('it match')
            self.location = value
        else:
            print('It is not rack!')
