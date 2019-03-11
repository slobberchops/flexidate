# Copyright 2019 Rafe Kaplan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import enum
import functools
import math


class Precision(enum.Enum):
    day = 1
    month = 2
    year = 3
    none = 4


@functools.total_ordering
class Fuzidate:

    max = None  # type: datetime.date
    min = None  # type: datetime.date
    unknown = None  # type: datetime.date

    @property
    def number(self) -> int:
        return self.__number

    @property
    def year(self) -> int:
        return math.floor(self.__number / 10000)

    @property
    def month(self) -> int:
        return (math.floor(self.__number / 100)) % 100

    @property
    def day(self) -> int:
        return self.__number % 100

    @property
    def precision(self) -> Precision:
        if not self.year:
            return Precision.none
        elif not self.month:
            return Precision.year
        elif not self.day:
            return Precision.month
        else:
            return Precision.day

    def __init__(self, number: int):
        self.__number = number

    @classmethod
    def from_date(cls, date: datetime.date) -> 'Fuzidate':
        return cls(date_to_number(date))

    @classmethod
    def compose(cls, year=0, month=0, day=0):
        return cls(day + (month * 100) + (year * 10000))

    def __eq__(self, other) -> bool:
        if type(self) is not type(other):
            return NotImplemented
        return self.__number == other.__number

    def __lt__(self, other) -> bool:
        if type(self) is not type(other):
            return NotImplemented
        return self.__number < other.__number

    def __str__(self):
        precision = self.precision
        if precision is Precision.none:
            return 'unknown'
        elif precision is Precision.year:
            return str(self.year)
        elif precision is Precision.month:
            return '{}-{:02d}'.format(self.year, self.month)
        else:
            return '{}-{:02d}-{:02d}'.format(self.year, self.month, self.day)

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, self.__number)


def date_to_number(date: datetime.date) -> Fuzidate:
    """
    Convert date to fuzidate number representation.

    Args:
        date: A date.

    Returns:
        Number Representation of date as an int number. For example,
        Nov 11th 1918 is represented as 19181111.
    """
    return date.day + date.month * 100 + date.year * 10000


Fuzidate.max = Fuzidate.from_date(datetime.date.max)
Fuzidate.min = Fuzidate(datetime.date.min.year * 10000)
Fuzidate.unknown = Fuzidate(0)


__all__ = [
    date_to_number.__name__,
    Fuzidate.__name__,
    Precision.__name__,
]
