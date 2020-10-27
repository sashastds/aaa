import string
import numpy as np
import re
from itertools import chain
from collections import Counter
from typing import List, Union


class BaseTokenizer():
    
    def __init__(self, separator = ' '):
        
        """
        base tokenizer which splits by a stated separator
        """
        
        self._separator = separator
        
        pass
    
    @property
    def separator(self):
        
        return self._separator
    
    @separator.setter
    def separator(self, separator: str):
        
        self._separator = separator
        
    def preprocess(self, text: str) -> str:
        """
        leave input text as is
        """
        
        #raise NotImplementedError('preprocessing is not implemented for BaseTokenizer')
        return text
        
    def split(self, text: str) -> List[str]:
        
        """
        splits 'text' and returns only non-zero lengths chunks in a list
        """
        
        if len(self._separator) > 0:
            splitted = text.split(self._separator)
        else:
            splitted = list(text)
        
        return [s for s in splitted if len(s) > 0]
        
            
    def texts_to_sequences(self, texts: List[str]) -> List[List[str]]:
        """
        splits every string in texts into several using separator
        returns list of lists
        """
        return [self.split(self.preprocess(text)) for text in texts]
    
    
class Tokenizer(BaseTokenizer):
    
    """
    tokenizer which splits by a stated 'separator' after cleaning all 'punctuation', urls and numbers
    might also convert to 'lowercase' if True
    """
    
    def __init__(self, separator = ' ', punctuation = string.punctuation, lowercase = True):
        
        
        super().__init__(separator)
        
        self._punctuation = ''.join([s for s in punctuation if s!= separator])
        
        ### this does not create additional empty strings but might concatenate words like in "hey,you" -> "heyyou"
        #self._translation_table = str.maketrans('', '', self._punctuation)
        
        ### this doing the reversed thing and e.g. 'what!?really' might become 'what<sep><sep>really'
        ### but using custom split we fixing it
        if len(separator) > 0:
            self._translation_table = str.maketrans(self._punctuation, separator * len(self._punctuation))
        else:
            self._translation_table = str.maketrans('', '', self._punctuation)
            
        self._lowercase = lowercase

        self.URL_REGEXP = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
        self.NUM_REGEXP = r'[0-9]{1,}'
        
 
    @property
    def separator(self):
        
        return super().separator

    @separator.setter
    def separator(self, separator: str):
        """
        allows to change separator but also changes punctuation and translation table to avoid collisions
        """
        self._separator = separator
        self._punctuation = ''.join([s for s in self._punctuation if s!= separator])
        
        if len(separator) > 0:
            self._translation_table = str.maketrans(self._punctuation, separator * len(self._punctuation))
        else:
            self._translation_table = str.maketrans('', '', self._punctuation)
        
    @property
    def lowercase(self):
        
        return self._lowercase
    
    @lowercase.setter
    def lowercase(self, lowercase):
        
        self._lowercase = lowercase
        
    @property
    def punctuation(self):
        
        return self._punctuation
    
    @punctuation.setter
    def punctuation(self, punctuation):
        
        raise AttributeError('you cannot reset this attribute as it might conflict with separator - use class constructor')
    
    
    def preprocess(self, text: str) -> str:
        
        
        """
        preprocess text using two kind of regexps
        punctuation is also removed after
        returns preprocessed text as string 
        """
        
        if self._lowercase:
            
            text = text.lower()
        
        text = re.sub(pattern = self.URL_REGEXP, string = text, repl = '')
        text = re.sub(pattern = self.NUM_REGEXP, string = text, repl = '')  
        text = text.translate(self._translation_table)
        
        return text
    
    def texts_to_sequences(self, texts: List[str]) -> List[List[str]]:
        """
        splits every string in texts into several using separator
        returns list of lists
        """        
        
        return super().texts_to_sequences(texts)
