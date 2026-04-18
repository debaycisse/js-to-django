from typing import TypedDict
from collections.abc import Mapping


class StringProperties(TypedDict):
    '''
    String's property type
    '''
    length: int
    is_palindrome: bool
    unique_characters: int
    word_count: int
    sha256_hash: str
    character_frequency_map: Mapping[str, int]

class StringTypeHintError(TypedDict):
    '''
    String's property error type
    '''
    error: Mapping[str, str]

