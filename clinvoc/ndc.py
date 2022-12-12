from .base import left_pad, RegexVocabulary, LexiconVocabulary, MedicationVocabulary
from operator import add
from toolz.curried import partial
from itertools import product
import os
from clinvoc.resources import resources
import csv
from six.moves import reduce
from six import next

def _read_text_file(filename):
    with open(filename, 'rt') as infile:
        reader = csv.reader(infile, delimiter='\t')
        next(reader)
        _all_ndc_codes = [row[2] for row in reader]
    return _all_ndc_codes

_all_ndc_codes = _read_text_file(os.path.join(resources, 'ndctext', 'package.txt'))
        
class NDC(RegexVocabulary, LexiconVocabulary, MedicationVocabulary): # Diamond inheritance!
    vocab_name = 'NDC'
    def __init__(self):
        RegexVocabulary.__init__(self, r'([\d\*]{1,5}\-[a-zA-Z\d\*]{1,4}\-(([\d\*]{1,2})|([a-zA-Z\*][\d\*]?)|(0[a-zA-Z\*])))|([\d\*]{4,9}[a-zA-Z\d\*]{1,2})')
        LexiconVocabulary.__init__(self, map(self.standardize, _all_ndc_codes))
    
    def _match_pattern(self, pattern):
        return set(map(self.standardize, 
                       set(map(partial(reduce, add), product(*map(lambda x: [x] if x != '*' else list(map(str, range(10))), 
                                                                  pattern))))))
    
    def _standardize(self, code):
        if '-' not in code:
            return left_pad(code, 11)
        part1, part2, part3 = code.split('-')
        part1 = left_pad(part1, 5)
        part2 = left_pad(part2, 4)
        part3 = left_pad(part3, 2)
        return part1 + part2 + part3
    
    def _fill_range(self, start, end):
        raise NotImplementedError('NDC does not support range filling')
    
    
