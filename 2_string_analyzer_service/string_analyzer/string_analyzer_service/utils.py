from django.db import models
from datetime import datetime, timezone
from hashlib import sha256
from . import types_util as tu


def created_at() -> str:
    '''
    Computes and returns the ISO format of the current time
    '''
    return datetime.now(timezone.utc)\
        .isoformat(timespec='milliseconds')\
            .replace('+00:00', 'Z')

def obtain_id(string_object: str) -> str:
    '''
    Computes and returns hash value of a given string object
    '''
    return sha256(string_object.encode('utf-8')).hexdigest()


# Class for managing string object
class StringProperties:
    '''Represents an instance of a string object and its properties'''
    def __init__(self, string_value:str) -> None:
        '''Initializes an instance for this class'''
        self.value:str = string_value
        self.length:int = len(string_value)
    
    def is_palindrome(self) -> bool:
        '''
        Computes and returns if the value attribute of an
        instance is a palindrome string or not
        '''
        reversed_string:str = self.__revers_string()
        for ch1, ch2 in zip(self.value, reversed_string):
            if ch1 != ch2:
                return False
        return True
    
    def get_unique_characters_count(self) -> int:
        '''
        Computes and returns the total number of unique characters,
        found in the value attribute of an instance
        '''
        character_store:list[str] = []
        counter:int = 0

        for ch in self.value:
            if ch not in character_store:
                character_store.append(ch)
                counter += 1
        return counter

    def get_char_freq_map(self) -> dict[str, int]:
        '''
        Computes and returns mapping of various characters, found
        in the value attribute of an instance and their occurences
        counts
        '''
        character_store: dict[str, int] = {}
        for ch in self.value:
            if ch in character_store.keys():
                character_store[ch] += 1
            else:
                character_store[ch] = 1
        return character_store
    
    def get_word_counts(self) -> int:
        '''
        Computes and returns the total number of words, found
        in the value attribute of an instance
        '''
        string_words:list[str] = self.value.split(' ')
        return len(string_words)
    
    def get_sha256(self) -> str:
        '''Computes and returns hash value of the value attribute'''
        return sha256(self.value.encode('utf-8')).hexdigest()
    
    def __revers_string(self) -> str:
        '''
        Creates and returns a reversed version of the
        value attribute of an instance
        '''
        rev_string:str = ''
        counter:int = len(self.value)
        while counter > 0:
            counter -= 1
            rev_string += self.value[counter]
        return rev_string
