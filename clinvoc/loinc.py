import csv
from .base import Vocabulary, create_bisection_range_filler, create_fnmatch_wildcard_matcher
import os
from .resources import resources
from toolz.functoolz import compose


def read_text_file(filename):
    codes = []
    with open(filename, 'rb') as infile:
        reader = csv.reader(infile, delimiter=',', quoting=csv.QUOTE_ALL)
        reader.next()
        for line in reader:
            codes.append(line[0])
    return codes

def split_and_sort_codes(codes):
    splitted = [tuple(int(x) for x in code.split('-')) for code in codes]
    splitted.sort()
#     joined = [str(pair[0]) + '-' + str(pair[1]) for pair in splitted]
    return splitted

def join_codes(codes):
    return ['-'.join(map(str, pair)) for pair in codes]

all_splitted_loinc_codes = split_and_sort_codes(read_text_file(os.path.join(resources, 'LOINC_2.59_Text', 'loinc.csv')))
all_loinc_codes = join_codes(all_splitted_loinc_codes)
splitted_range_filler = create_bisection_range_filler(all_splitted_loinc_codes, 'splitted_range_filler')
pattern_matcher = create_fnmatch_wildcard_matcher(all_loinc_codes, 'pattern_matcher')
class LOINC(Vocabulary):
    @staticmethod
    def _fill_range(lower, upper):
        codes = splitted_range_filler(tuple(map(int, lower.split('-'))), tuple(map(int, upper.split('-')))) 
        return join_codes(codes)
    
    def parse(self, expression, delimiter=',;\s', range_delimiter='->'):
        return Vocabulary.parse(self, expression, delimiter=delimiter, range_delimiter=range_delimiter)
    
    @staticmethod
    def _match_pattern(pattern):
        return pattern_matcher(pattern)
        
    def standardize(self, code):
        # Remove leading zeroes
        return code.lstrip('0')
        
