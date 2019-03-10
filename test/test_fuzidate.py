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

import fuzidate

ARMISTICE = datetime.date(1918, 11, 11)
ARMISTICE_FZD = fuzidate.Fuzidate(19181111)


def test_number():
    number = fuzidate.Fuzidate(19181111).number
    assert number == 19181111


def test_date_to_number():
    assert fuzidate.date_to_number(ARMISTICE) == 19181111


def test_from_date():
    assert fuzidate.Fuzidate.from_date(ARMISTICE).number == 19181111
