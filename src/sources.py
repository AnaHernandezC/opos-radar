from ayuntamiento_valladolid import AyuntamientoValladolidSource
from age import AgeSource
from aena import AenaSource
from adif import AdifSource

SOURCES = [
    AyuntamientoValladolidSource(),
    AgeSource(),
    AenaSource(),
    AdifSource(),
]
