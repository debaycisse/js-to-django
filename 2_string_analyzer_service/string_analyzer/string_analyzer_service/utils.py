from rest_framework import status
from datetime import datetime, timezone
from hashlib import sha256
from . import custom_http_exceptions as cte

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

def validate_query_params(
        condition: bool, 
        detail: str = 'Invalid query parameter values or types'
    ):
    '''
    Validates a given query parameter and
    decides if it is valid or not (by raising an exception)

    Args:
        condition - a condition, used to make a decision
        detail - description, used to describe every failed condition
    '''
    if condition is True:
        raise cte.CustomException400(detail=detail)
    
def validate_filters(
        condition: bool, 
        detail: str = 'Query parsed but resulted in conflicting filters'
    ):
    '''
    Validates a given filter object and decides if it is valid
    or not (by raising an exception)

    Args:
        condition - a condition, used to make a decision
        detail - description, used to describe every failed condition
    '''
    if condition is True:
        raise cte.CustomException422(detail=detail)


def get_filters(query: str | None = None):
    '''
    Obtains filtering object from a given string by
    extracting keywords from it to make up the object

    Args:
        query - the query which contains the natural statement
        from which keywords are extracted to make up a filtering object
    '''
    query_filter: dict | dict[str, str | int | bool] = FilterString(query=query)
    return query_filter.filter()


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


class FilterString:
    '''
    Manages keywords extractions from string, received from
    query parameter of an HTTP request
    '''
    def __init__(self, query: str = None):
        if query is not None:
            self.query = query
            self.q_list = query.split(' ')
        else:
            self.query = None
        self.filters = {}
    
    def __word_count_extract(self):
        '''
        Extracts and parses the word count
        '''
        if self.query.__contains__('word'):
            self.filters['word_count'] = 1
        elif self.query.__contains__('words'):
            num_value = self.q_list[self.q_list.index('words') - 1]
            self.filters['word_count'] = num_value

    def __palindromic_extract(self):
        '''
        Extracts and parses palindrome's given value
        '''
        if self.query.__contains__('palindromic'):
            self.filters['is_palindrome'] = True

    def __min_length_extract(self):
        '''
        Extracts and parses minimum length value
        '''
        if (
            self.query.__contains__('longer than') or \
            self.query.__contains__('greater than')
        ) and \
            self.query.__contains__('characters'):
            num_value = self.\
                q_list[self.q_list.index('characters') - 1]
            self.filters['min_length'] = int(num_value) + 1

    def __max_length_extract(self):
        '''
        Extracts and parses maximum length value
        '''
        if (
            self.query.__contains__('shorter than') or \
            self.query.__contains__('lesser than') or \
            self.query.__contains__('less than')
        ) and self.query.__contains__('characters'):
            num_value = self.\
                q_list[self.q_list.index('characters') - 1]
            self.filters['max_length'] = num_value

    def __contains_character_extract(self):
        '''
        Extracts and parses contained characters
        '''
        if self.query.__contains__('contain') and \
            self.query.__contains__('vowel'):
            value = self.q_list[self.q_list.index('vowel') - 1]
            if value == 'first' or value == '1st':
                self.filters['contains_character'] = 'a'
            elif value == 'second' or value == '2nd':
                self.filters['contains_character'] = 'e'
            elif value == 'third' or value == '3rd':
                self.filters['contains_character'] = 'i'
            elif value == 'fourth' or value == '4th':
                self.filters['contains_character'] = 'o'
            elif value == 'fifth' or value == '5th':
                self.filters['contains_character'] = 'u'
        elif self.query.__contains__('contain') and self.query.__contains__('letter'):
            value = self.q_list[self.q_list.index('letter') + 1]
            self.filters['contains_character'] = value

    def filter(self):
        '''
        Carries out all the extracts to create a filter object that
        contains all the extracted keywords and values
        '''
        if self.query is not None:
            self.__palindromic_extract()
            self.__word_count_extract()
            self.__min_length_extract()
            self.__max_length_extract()
            self.__contains_character_extract()
        return self.filters
