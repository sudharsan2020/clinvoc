import re
from .base import RegexVocabulary, NoWildcardsVocabulary, NoCheckVocabulary, RevenueSourceVocabulary

_ubrev_split_regex = re.compile('([0-9]+)([A-z]*)')
def _ubrev_split(code):
    match = _ubrev_split_regex.match(code)
    number_part = match.groups()[0]
    letter_part = match.groups()[1]
    return number_part, letter_part

def _ubrev_join(number_part, letter_part):
    digits = 4 - len(letter_part)
    return (('%%.%dd' % digits) % int(number_part)) + letter_part

class UBREV(RegexVocabulary, NoWildcardsVocabulary, NoCheckVocabulary, RevenueSourceVocabulary):
    vocab_name = 'UBREV'
    def __init__(self):
        RegexVocabulary.__init__(self, '[\d]{1,2}\.?(([\d]{1,2})|([\d][A-z]))')
    
    @staticmethod
    def _fill_range(start, end):
        start_number, start_letter = _ubrev_split(start)
        end_number, end_letter = _ubrev_split(end)
        assert start_letter == end_letter
        return [
            _ubrev_join(num, start_letter)
            for num in range(int(start_number), int(end_number) + 1)
        ]
    
    @staticmethod
    def _standardize(code):
        return _ubrev_join(*_ubrev_split(code))
