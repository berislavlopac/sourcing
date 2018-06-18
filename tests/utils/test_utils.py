from sourcing.utils import get_all_subclasses
from tests.utils.classes import *
from tests.utils.classes.subclasses import *


def test_get_all_subclasses():
    subclasses = get_all_subclasses(BaseClass)
    assert NotASubclass not in subclasses
    assert BaseClass not in subclasses
    assert subclasses == {
        Level1Subclass,
        Level1SubclassA,
        Level1SubclassB,
        Level2Subclass,
        Level3Subclass
    }


def test_get_all_subclasses_inclusive():
    subclasses = get_all_subclasses(BaseClass, inclusive=True)
    assert NotASubclass not in subclasses
    assert subclasses == {
        BaseClass,
        Level1Subclass,
        Level1SubclassA,
        Level1SubclassB,
        Level2Subclass,
        Level3Subclass
    }
