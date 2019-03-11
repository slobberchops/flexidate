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

OUTBREAK = datetime.date(1914, 7, 28)
OUTBREAK_FZD = fuzidate.Fuzidate(19140728)


def test_date_to_number():
    assert fuzidate.date_to_number(OUTBREAK) == 19140728


def test_from_date():
    assert fuzidate.Fuzidate.from_date(OUTBREAK).number == 19140728


def test_constants():
    assert fuzidate.Fuzidate.max.number == 99991231
    assert fuzidate.Fuzidate.min.number == 10000
    assert fuzidate.Fuzidate.unknown.number == 0


class TestProperties:

    @staticmethod
    def test_number():
        assert OUTBREAK_FZD.number == 19140728

    @staticmethod
    def test_year():
        assert OUTBREAK_FZD.year == 1914

    @staticmethod
    def test_year_missing():
        assert fuzidate.Fuzidate.unknown.year == 0

    @staticmethod
    def test_month():
        assert OUTBREAK_FZD.month == 7

    @staticmethod
    def test_month_missing():
        assert fuzidate.Fuzidate(19140000).month == 0

    @staticmethod
    def test_day():
        assert OUTBREAK_FZD.day == 28

    @staticmethod
    def test_day_missing():
        assert fuzidate.Fuzidate(19140700).day == 0

    class TestPrecision:

        @staticmethod
        def test_none():
            assert (fuzidate.Fuzidate.unknown.precision is
                    fuzidate.Precision.none)

        @staticmethod
        def test_year():
            assert (fuzidate.Fuzidate(19180000).precision is
                    fuzidate.Precision.year)

        @staticmethod
        def test_month():
            assert (fuzidate.Fuzidate(19180700).precision is
                    fuzidate.Precision.month)

        @staticmethod
        def test_day():
            assert (fuzidate.Fuzidate(19180728).precision is
                    fuzidate.Precision.day)


class TestToString:

    def test_repr(self):
        assert repr(fuzidate.Fuzidate.unknown) == 'Fuzidate(0)'
        assert repr(OUTBREAK_FZD) == 'Fuzidate(19140728)'

    class TestStr:

        def test_unknown(self):
            assert str(fuzidate.Fuzidate.unknown) == 'unknown'

        def test_year(self):
            assert str(fuzidate.Fuzidate(19140000)) == '1914'
            assert str(fuzidate.Fuzidate(100000)) == '10'

        def test_month(self):
            assert str(fuzidate.Fuzidate(19140700)) == '1914-07'

        def test_day(self):
            assert str(fuzidate.Fuzidate(19140701)) == '1914-07-01'


class TestOrder:

    class TestEq:

        @staticmethod
        def test_invalid_eq_type():
            assert OUTBREAK_FZD != 19140728
            assert 19140728 != OUTBREAK_FZD

        @staticmethod
        def test_is_same():
            assert OUTBREAK_FZD == OUTBREAK_FZD

        @staticmethod
        def test_is_eq():
            assert OUTBREAK_FZD == fuzidate.Fuzidate(19140728)

        @staticmethod
        @pytest.mark.parametrize('number', [19181111, 19140700, 19140000, 0])
        def test_is_ne(number):
            assert OUTBREAK_FZD != fuzidate.Fuzidate(number)

    class TestLt:

        @staticmethod
        def test_invalid_lt_type():
            with pytest.raises(TypeError):
                assert OUTBREAK_FZD < 19140728
            with pytest.raises(TypeError):
                assert 19140728 < OUTBREAK_FZD

        @staticmethod
        @pytest.mark.parametrize('number', [19140729, 19140800, 19150000])
        def test_is_lt(number):
            assert OUTBREAK_FZD < fuzidate.Fuzidate(number)

        @staticmethod
        @pytest.mark.parametrize('number', [19140727, 19140700, 19140000])
        def test_is_ge(number):
            assert OUTBREAK_FZD >= fuzidate.Fuzidate(number)


class TestCompose:

    def test_default(self):
        assert fuzidate.Fuzidate.compose() == fuzidate.Fuzidate.unknown

    def test_year(self):
        assert fuzidate.Fuzidate.compose(1914) == fuzidate.Fuzidate(19140000)

    def test_month(self):
        assert (fuzidate.Fuzidate.compose(1914, 7) ==
                fuzidate.Fuzidate(19140700))

    def test_day(self):
        assert (fuzidate.Fuzidate.compose(1914, 7, 28) ==
                fuzidate.Fuzidate(19140728))
