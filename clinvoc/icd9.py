import os
from .resources import resources
from .base import left_pad, ProcedureVocabulary, DiagnosisVocabulary
from .icd import ICDBase

def _read_text_file(filename):
    result = []
    with open(filename, 'rt') as infile:
        result.extend(line[:5] for line in infile)
    return result

def _standardize_icd9_cm(code, use_decimals=False):
    code_ = code.strip().upper()
    if use_decimals:
        pre_len = 4 if code_[0] == 'E' else 3
        if '.' not in code_:
            return left_pad(code_, pre_len)
        pre, post = code_.split('.')
        result = f'{left_pad(pre, pre_len)}.{post}'
    elif code_[0] == 'V' or code_[0] != 'E':
        result = code_[:3]
        if len(code_) > 3:
            result += f'.{code_[3:]}'
    else:
        result = code_[:4]
        if len(code_) > 4:
            result += f'.{code_[4:]}'
    return result

def _standardize_icd9_pcs(code, use_decimals=False):
    code_ = code.strip().upper()
    if use_decimals:
        if '.' in code_:
            pre, post = code_.split('.')
            result = f'{left_pad(pre, 2)}.{post}'
        else:
            result = left_pad(code_, 2)
    else:
        result = code_[:2]
        if len(code_) > 2:
            result += f'.{code_[2:]}'
    return result

_all_icd9_cm_codes = list(map(_standardize_icd9_cm, _read_text_file(os.path.join(resources, 'CMS32_DESC_SHORT_DX.txt'))))
_all_icd9_pcs_codes = list(map(_standardize_icd9_pcs, _read_text_file(os.path.join(resources, 'CMS32_DESC_SHORT_SG.txt'))))

class ICD9CM(ICDBase, DiagnosisVocabulary):
    vocab_name = 'ICD9CM'
    decimal_regex = '(%s)|(%s)|(%s)' % ('V[\d\*]{2}(\.[\d\*]{1,2})?', 
                                        'E[\d\*]{3}(\.[\d\*]{1})?', 
                                        '[\d\*]{1,3}(\.[\d\*]{1,2})?')
    nondecimal_regex = '(%s)|(%s)|(%s)' % ('V[\d\*]{2,4}', 
                                           'E[\d\*]{3,4}', 
                                           '[\d\*]{3,5}')
    pre_lexicon = _all_icd9_cm_codes
    def _standardize(self, code):
        return _standardize_icd9_cm(code, self.use_decimals)

class ICD9PCS(ICDBase, ProcedureVocabulary):
    vocab_name = 'ICD9PCS'
    decimal_regex = '[\d\*]{1,2}(\.[\d\*]{1,3})?'
    nondecimal_regex = '[\d\*]{2,5}'
    pre_lexicon = _all_icd9_pcs_codes
    def _standardize(self, code):
        return _standardize_icd9_pcs(code, self.use_decimals)

