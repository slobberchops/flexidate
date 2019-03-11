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

import fuzidate as fzd

OUTBREAK = datetime.date(1914, 7, 28)
OUTBREAK_FZD = fzd.Fuzidate(19140728)


def test_date_to_number():
    assert fzd.date_to_number(OUTBREAK) == 19140728


def test_from_date():
    assert fzd.Fuzidate.from_date(OUTBREAK).number == 19140728


def test_constants():
    assert fzd.Fuzidate.max.number == 99991231
    assert fzd.Fuzidate.min.number == 10000
    assert fzd.Fuzidate.unknown.number == 0


class TestPrecisionOrder:

    @staticmethod
    @pytest.mark.parametrize('prec', [sorted(fzd.Precision)])
    def test_eq(prec):
        assert prec == prec

    @staticmethod
    @pytest.mark.parametrize('index',
                             list(range(len(fzd.Precision))))
    def test_not_eq(index):
        precisions = list(fzd.Precision)
        l = precisions[index]
        r = precisions[(index + 1) % len(fzd.Precision)]
        assert l != r

    @staticmethod
    @pytest.mark.parametrize('index',
                             list(range(len(fzd.Precision) - 1)))
    def test_lt(index):
        precisions = list(fzd.Precision)
        l = precisions[index]
        r = precisions[index + 1]
        assert l < r

    def test_lt_invalid(self):
        with pytest.raises(TypeError):
            fzd.Precision.day < 1


class TestProperties:

    @staticmethod
    def test_number():
        assert OUTBREAK_FZD.number == 19140728

    @staticmethod
    def test_year():
        assert OUTBREAK_FZD.year == 1914

    @staticmethod
    def test_year_missing():
        assert fzd.Fuzidate.unknown.year == 0

    @staticmethod
    def test_month():
        assert OUTBREAK_FZD.month == 7

    @staticmethod
    def test_month_missing():
        assert fzd.Fuzidate(19140000).month == 0

    @staticmethod
    def test_day():
        assert OUTBREAK_FZD.day == 28

    @staticmethod
    def test_day_missing():
        assert fzd.Fuzidate(19140700).day == 0

    class TestPrecision:

        @staticmethod
        def test_none():
            assert fzd.Fuzidate.unknown.precision is fzd.Precision.none

        @staticmethod
        def test_year():
            assert fzd.Fuzidate(19180000).precision is fzd.Precision.year

        @staticmethod
        def test_month():
            assert fzd.Fuzidate(19180700).precision is fzd.Precision.month

        @staticmethod
        def test_day():
            assert fzd.Fuzidate(19180728).precision is fzd.Precision.day


class TestToString:

    def test_repr(self):
        assert repr(fzd.Fuzidate.unknown) == 'Fuzidate(0)'
        assert repr(OUTBREAK_FZD) == 'Fuzidate(19140728)'

    class TestStr:

        def test_unknown(self):
            assert str(fzd.Fuzidate.unknown) == 'unknown'

        def test_year(self):
            assert str(fzd.Fuzidate(19140000)) == '1914'
            assert str(fzd.Fuzidate(100000)) == '10'

        def test_month(self):
            assert str(fzd.Fuzidate(19140700)) == '1914-07'

        def test_day(self):
            assert str(fzd.Fuzidate(19140701)) == '1914-07-01'


class TestFuzidateOrder:

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
            assert OUTBREAK_FZD == fzd.Fuzidate(19140728)

        @staticmethod
        @pytest.mark.parametrize('number', [19181111, 19140700, 19140000, 0])
        def test_is_ne(number):
            assert OUTBREAK_FZD != fzd.Fuzidate(number)

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
            assert OUTBREAK_FZD < fzd.Fuzidate(number)

        @staticmethod
        @pytest.mark.parametrize('number', [19140727, 19140700, 19140000])
        def test_is_ge(number):
            assert OUTBREAK_FZD >= fzd.Fuzidate(number)


class TestCompose:

    @staticmethod
    def test_default():
        assert fzd.Fuzidate.compose() == fzd.Fuzidate.unknown

    @staticmethod
    def test_year():
        assert fzd.Fuzidate.compose(1914) == fzd.Fuzidate(19140000)

    @staticmethod
    def test_month():
        assert fzd.Fuzidate.compose(1914, 7) == fzd.Fuzidate(19140700)

    @staticmethod
    def test_day():
        assert fzd.Fuzidate.compose(1914, 7, 28) == fzd.Fuzidate(19140728)


class TestUsingPrecision:

    @staticmethod
    def test_none():
        unknown = OUTBREAK_FZD.using(fzd.Precision.none)
        assert unknown is fzd.Fuzidate.unknown

    @staticmethod
    def test_less_precise_year():
        year = OUTBREAK_FZD.using(fzd.Precision.year)
        assert year == fzd.Fuzidate.compose(1914)

    @staticmethod
    def test_less_precise_month():
        month = OUTBREAK_FZD.using(fzd.Precision.month)
        assert month == fzd.Fuzidate.compose(1914, 7)

    @staticmethod
    def test_less_precise_day():
        day = OUTBREAK_FZD.using(fzd.Precision.day)
        assert day == fzd.Fuzidate.compose(1914, 7, 28)

    @staticmethod
    def test_more_precise_year():
        unknown = fzd.Fuzidate.unknown
        year = unknown.using(fzd.Precision.year)
        assert year == fzd.Fuzidate.compose(1)

    @staticmethod
    def test_more_precise_month():
        unknown = fzd.Fuzidate.unknown
        month = unknown.using(fzd.Precision.month)
        assert month == fzd.Fuzidate.compose(1, 1)

    @staticmethod
    def test_more_precise_day():
        unknown = fzd.Fuzidate.unknown
        day = unknown.using(fzd.Precision.day)
        assert day == fzd.Fuzidate.compose(1, 1, 1)
