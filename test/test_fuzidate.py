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

import pytest

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


class TestOrder:

    class TestEq:

        @staticmethod
        def test_invalid_eq_type():
            assert ARMISTICE_FZD != 19181111
            assert 19181111 != ARMISTICE_FZD

        @staticmethod
        def test_is_same():
            assert ARMISTICE_FZD == ARMISTICE_FZD

        @staticmethod
        def test_is_eq():
            assert ARMISTICE_FZD == fuzidate.Fuzidate(19181111)

        @staticmethod
        @pytest.mark.parametrize('number', [19140728, 19181100, 19180000, 0])
        def test_is_ne(number):
            assert ARMISTICE_FZD != fuzidate.Fuzidate(number)

    class TestLt:

        @staticmethod
        def test_invalid_lt_type():
            with pytest.raises(TypeError):
                assert ARMISTICE_FZD < 19181111
            with pytest.raises(TypeError):
                assert 19181111 < ARMISTICE_FZD

        @staticmethod
        @pytest.mark.parametrize('number', [19181112, 19181200, 19190000])
        def test_is_lt(number):
            assert ARMISTICE_FZD < fuzidate.Fuzidate(number)

        @staticmethod
        @pytest.mark.parametrize('number', [19181111, 19181100, 19180000])
        def test_is_ge(number):
            assert ARMISTICE_FZD >= fuzidate.Fuzidate(number)
