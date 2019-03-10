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


def date_to_number(date: datetime.date):
    """
    Convert date to fuzidate number representation.

    Args:
        date: A date.

    Returns:
        Number Representation of date as an int number. For example,
        Nov 11th 1918 is represented as 19181111.
    """
    return date.day + date.month * 100 + date.year * 10000


class Fuzidate:

    @property
    def number(self)->int:
        return self.__number

    def __init__(self, number: int):
        self.__number = number

    @classmethod
    def from_date(cls, date: datetime.date):
        return cls(date_to_number(date))


Fuzidate.max = Fuzidate.from_date(datetime.date.max)
Fuzidate.min = Fuzidate.from_date(datetime.date.min)


__all__ = [
    date_to_number.__name__,
    Fuzidate.__name__,
]
