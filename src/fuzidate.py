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

import calendar
import datetime
import enum
import functools
import math
import typing


class InvalidFuzidateError(Exception):
    """Raised when fuzidate is invalid."""


@functools.total_ordering
class Precision(enum.Enum):
    none = 1
    year = 2
    month = 3
    day = 4

    def __lt__(self, other):
        if not isinstance(other, Precision):
            return NotImplemented
        return self.value < other.value


@functools.total_ordering
class Fuzidate:

    max = None  # type: ClassVar[datetime.date]
    min = None  # type: ClassVar[datetime.date]
    unknown = None  # type: ClassVar[datetime.date]
    __high = None
    __low = None
    __validated = False

    @property
    def number(self) -> int:
        return self.__number

    @property
    def offset(self) -> int:
        return self.__offset

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
    def is_valid(self) -> bool:
        try:
            self.check_valid()
        except InvalidFuzidateError:
            return False
        else:
            return True

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

    @property
    def high(self) -> datetime.date:
        self.check_valid()
        return self.__high

    @property
    def low(self) -> datetime.date:
        if not self.__low:
            self.check_valid()
            self.__low = datetime.date(self.year or datetime.date.min.year,
                                       self.month or 1,
                                       self.day or 1)
        return self.__low

    @property
    def range(self) -> typing.Tuple[datetime.date, datetime.date]:
        return self.low, self.high

    def __init__(self, number: int, offset: int=0):
        self.__number = number
        self.__offset = offset

    @staticmethod
    def __calc_high(precision, year, month, day, offset):
        if precision < Precision.month:
            month = 12

        if precision < Precision.day:
            day = calendar.monthrange(year, month)[1]

        if offset:
            if precision is Precision.year:
                year += offset
            elif precision is Precision.month:
                high_months = month + offset
                year += int((high_months - 1) / 12)
                month = high_months % 12
                if not month:
                    month = 12
                try:
                    day = calendar.monthrange(year, month)[1]
                except ValueError:
                    raise InvalidFuzidateError('Offset out of range') from None
            elif precision is Precision.day:
                delta = datetime.timedelta(seconds=offset * (60 * 60 * 24))
                d = datetime.date(year, month, day)
                try:
                    high = d + delta
                except OverflowError:
                    raise InvalidFuzidateError('Offset out of range') from None
                else:
                    return high

        try:
            return datetime.date(year, month, day)
        except ValueError:
            raise InvalidFuzidateError('Offset out of range') from None

    def check_valid(self):
        if self.__validated:
            return

        offset = self.__offset
        if not self.__number:
            if offset:
                raise InvalidFuzidateError(
                    'Unknown fuzidate may not have offset')

            self.__high = datetime.date.max
            self.__validated = True
            return

        day = self.day
        precision = self.precision

        # Check basic number construction.
        if precision < Precision.day:
            if day:
                raise InvalidFuzidateError('Day must not be set')

        month = self.month
        if precision < Precision.month:
            if month:
                raise InvalidFuzidateError('Month must not be set')

        # Check that values are in correct range.
        year = self.year
        if day:
            if day > calendar.monthrange(year, month)[1]:
                raise InvalidFuzidateError('Invalid day: {}'.format(day))

        if month:
            if month > 12:
                raise InvalidFuzidateError('Invalid month: {}'.format(month))

        if not (self.min.year <= year <= self.max.year):
            raise InvalidFuzidateError('Invalid year: {}'.format(year))

        if offset < 0:
            raise InvalidFuzidateError('Offset must not be negative')

        self.__high = self.__calc_high(precision, year, month, day, offset)

        self.__validated = True

    def using(self, precision: Precision) -> 'Fuzidate':
        if self.__offset:
            raise NotImplementedError
        self.check_valid()

        if precision is Precision.none:
            return self.unknown
        elif precision is Precision.year:
            return self.compose(self.year or self.min.year)
        elif precision is Precision.month:
            return self.compose(self.year or self.min.year,
                                self.month or 1)
        else:
            return self.compose(self.year or self.min.year,
                                self.month or 1,
                                self.day or 1)

    @classmethod
    def from_date(cls, date: datetime.date) -> 'Fuzidate':
        return cls(date_to_number(date))

    @classmethod
    def compose(cls, year=0, month=0, day=0, offset=0):
        if year < 0:
            raise ValueError('Year may not be < 0')
        if month < 0:
            raise ValueError('Month may not be < 0')
        if day < 0:
            raise ValueError('Day may not be < 0')
        return cls(day + (month * 100) + (year * 10000), offset)

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
        offset = self.offset

        year, month, day = self.year, self.month, self.day

        if not (year or month or day):
            if offset:
                return '0+' + str(offset)
            else:
                return '0'

        if offset:
            offset_str = '+{:d}'.format(offset)
        else:
            offset_str = ''

        if not (month or day):
            return '{}{}'.format(year, offset_str)
        elif not day and year:
            return '{}-{:02d}{}'.format(self.year, self.month, offset_str)
        else:
            return '{}-{:02d}-{:02d}{}'.format(self.year, self.month, self.day,
                                               offset_str)


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
    InvalidFuzidateError.__name__,
    Precision.__name__,
]
