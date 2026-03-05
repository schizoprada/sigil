# ~/sigil/src/sigil/sym/pred/__init__.py
from .prim import (
    NotNone, Truthy, Falsy,
    IsEmpty, NotEmpty, Always,
    Never, Inside, Has,
    notnone, truthy, falsy,
    isempty, notempty, always,
    never, inside, has
)

from .comp import (
    Equal, NotEqual,
    Greater, Less,
    GreaterEqual,
    LessEqual,
    Between, Index,
    equal, notequal,
    greater, less,
    greaterequal,
    lessequal,
    between, index,
    eq, neq, gt, lt,
    gte, lte, btw, idx
)

from .typed import (
    Instance, Subclass, OfType,
    instance, subclass, oftype
)
