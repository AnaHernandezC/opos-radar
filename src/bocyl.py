from age import AgeSource
from bocyl import BocylSource

sources = [
    BocylSource(),
    AgeSource(),
]

for source in sources:
    items = source.fetch()
