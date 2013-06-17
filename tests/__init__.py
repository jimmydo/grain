from grain import expect
from .utils import assert_raises, assert_raises_assertion


class ExpectedError(Exception):
    pass


class ActualError(Exception):
    pass


class TestExpect(object):
    def test_takes_one_argument(self):
        expect(None)

    def test_does_not_allow_zero_arguments(self):
        with assert_raises(TypeError):
            expect()


class TestExtend(object):
    def setup(self):
        class Extension(object):
            def some_method(self):
                pass

            @classmethod
            def some_classmethod(cls):
                pass
        self.extension = Extension

    def test_overrides_base_method(self):
        items = []

        class Extension(object):
            @staticmethod
            def fail():
                items.append('fail')

        expecter = expect.extend(Extension)
        expecter.fail()
        assert items == ['fail']

    def test_right_most_extension_takes_precedence(self):
        items = []

        class Extension(object):
            def some_method(self):
                items.append('method')

            @classmethod
            def some_classmethod(cls):
                items.append('classmethod')

        expecter = expect.extend(self.extension, Extension)
        expecter(None).some_method()
        expecter.some_classmethod()
        assert items == ['method', 'classmethod']


class TestFail(object):
    def test_raises_AssertionError(self):
        with assert_raises_assertion(''):
            expect.fail()


class TestEqual(object):
    def test_passes_for_equal_values(self):
        expect('apple').equal('apple')

    def test_fails_for_unequal_values(self):
        with assert_raises_assertion("Expected 'apple' == 'orange'"):
            expect('apple').equal('orange')


class TestNotEqual(object):
    def test_passes_for_unequal_values(self):
        expect('apple').not_equal('orange')

    def test_fails_for_equal_values(self):
        with assert_raises_assertion("Expected 'apple' != 'apple'"):
            expect('apple').not_equal('apple')


class TestIs(object):
    def test_passes_for_same_values(self):
        expect(False).is_(False)

    def test_fails_for_different_values(self):
        with assert_raises_assertion('Expected False is True'):
            expect(False).is_(True)


class TestIsNot(object):
    def test_passes_for_different_values(self):
        expect(False).is_not(True)

    def test_fails_for_same_values(self):
        with assert_raises_assertion('Expected False is not False'):
            expect(False).is_not(False)


class TestLess(object):
    def test_passes_for_larger_value(self):
        expect(10).less(11)

    def test_fails_for_smaller_value(self):
        with assert_raises_assertion('Expected 10 < 9'):
            expect(10).less(9)


class TestLessEqual(object):
    def test_passes_for_larger_value(self):
        expect(10).less_equal(11)

    def test_passes_for_equal_value(self):
        expect(10).less_equal(10)

    def test_fails_for_smaller_value(self):
        with assert_raises_assertion('Expected 10 <= 9'):
            expect(10).less_equal(9)


class TestGreater(object):
    def test_passes_for_smaller_value(self):
        expect(10).greater(9)

    def test_fails_for_larger_value(self):
        with assert_raises_assertion('Expected 10 > 11'):
            expect(10).greater(11)


class TestGreaterEqual(object):
    def test_passes_for_smaller_value(self):
        expect(10).greater_equal(9)

    def test_passes_for_equal_value(self):
        expect(10).greater_equal(10)

    def test_fails_for_larger_value(self):
        with assert_raises_assertion('Expected 10 >= 11'):
            expect(10).greater_equal(11)


class TestAlmostEqual(object):
    def test_passes_for_equal_values(self):
        expect(1.0000001).almost_equal(1.00000014)
        expect(1.0000001).almost_equal(1.00000006)

    def test_fails_for_unequal_values(self):
        with assert_raises_assertion(
                'Expected 1.0000001 almost equal to 1.00000016 (7)'):
            expect(1.0000001).almost_equal(1.00000016)


class TestNotAlmostEqual(object):
    def test_passes_for_unequal_values(self):
        expect(1.0000001).not_almost_equal(1.00000016)

    def test_fails_for_equal_values(self):
        with assert_raises_assertion(
                'Expected 1.0000001 not almost equal to 1.00000014 (7)'):
            expect(1.0000001).not_almost_equal(1.00000014)


class TestRaises(object):
    def test_passes_for_expected_exception(self):
        with expect.raises(ExpectedError):
            raise ExpectedError

    def test_fails_when_no_exception_is_raised(self):
        with assert_raises_assertion(
                "Expected code to raise <class 'tests.ExpectedError'>"):
            with expect.raises(ExpectedError):
                pass

    def test_allows_unexpected_exception_to_bubble_up(self):
        with assert_raises(ActualError, 'Unexpected exception should bubble up'):
            with expect.raises(ExpectedError):
                raise ActualError('Unexpected exception should bubble up')
