import string
import numpy as np
import re
from itertools import chain
from collections import Counter
from typing import List, Union
from .transformers import TfidfTransformer
    
    
class CountVectorizer():
    
    """
    can make vectorized form of text data using 'tokenizer'
    size of vocab can not exceed 'max_features' if set
    """
    
    VOCAB_ORDERINGS = set(['encounter', 'counts', 'alphabetical'])
    
    def __init__(self, tokenizer, max_features = None):
        
        self._tokenizer = tokenizer
        self._max_features = max_features
        self._feature_names = None
        self._vocab = None
        self._itos = None
        
    @property
    def tokenizer(self):
        
        return self._tokenizer
    
    @tokenizer.setter
    def tokenizer(self, tokenizer):
        self._tokenizer = tokenizer
        
    @property
    def max_features(self):
        
        return self._max_features
    
    @max_features.setter
    def max_features(self, max_features):
        
        self._max_features = max_features
        
    @property
    def num_features(self):
        
        return len(self._vocab)
    
    @num_features.setter
    def vocab_size(self, vocab_size):
        
        raise AttributeError('cannot reset "num_features" - only through fit')
        
    @property
    def vocab_size(self):
        
        return len(self._vocab)
    
    @vocab_size.setter
    def vocab_size(self, vocab_size):
        
        raise AttributeError('cannot reset "vocab_size" - only through fit')
        
    @property
    def vocab(self):
        
        return self._vocab
    
    @vocab.setter
    def vocab(self, vocab):
        
        raise AttributeError('cannot set "vocab" like that - only through fit')
        
    def stoi(self, s: str) -> int:
        
        """
        returns index of word in vocab or None if not in vocab
        """
        
        if self._vocab is None:
            
            raise ValueError('you should fit vectorizer first')
            
        else:
            
            return self._vocab.get(s, None) 
    
    def itos(self, i: int) -> str:
        
        """
        returns word in vocab by index or None if index is more than vocab_size or negative
        """
        
        if self._itos is None:
            
            raise ValueError('you should fit vectorizer first')
            
        else:
            
            return self._itos.get(i, None)     
          
    def fit(self, texts: List[str], min_count = 1, min_length = 1, ordering = 'counts'):
        
        """
        builds tokenizer's vocab
        'min_length' defines minimal acceptable token's length for including in the vocab
        'min_count' defines minimal acceptable number of counts for token in 'texts' corpus
        'ordering' actually applies only after 'max_features' is used through "counts" ordering
        """
        
        tokenized_texts = self.tokenizer.texts_to_sequences(texts)
            
        all_counts = Counter(chain(*tokenized_texts))

        ### enumerate is used only to later restore init encounter ordering if needed
        ### but we gotta restrict with 'max_features' using total counts in corpus
        ### sorting by counts first
        all_counts = sorted(enumerate(all_counts.items()), key = lambda x: -x[1][1])
        selected = [(i, (s, c)) for (i, (s, c)) in all_counts if len(s) >= min_length and c >= min_count][:self._max_features]
        
        ordering = ordering.lower()
        if ordering not in self.VOCAB_ORDERINGS:
            
            print(f'using default ordering by number of counts in corpus instead of "{ordering}"')
            ordering = 'counts'
        
        if ordering == 'counts':
        
            selected = [s for (i, (s, c)) in selected]
        
        elif ordering == 'alphabetical':
            
            selected = [s for (i, (s, c)) in sorted(selected, key = lambda x: x[1][0])]
        
        else:
            
            selected = [s for (i, (s, c)) in sorted(selected, key = lambda x: x[0])]
        
        self._itos = dict(enumerate(selected))
        self._vocab = {v:k for k, v in self._itos.items()}
        self._feature_names = list(self._vocab)
        
    
    def fit_transform(self, texts: List[str], min_count = 1, min_length = 1, ordering = 'counts',
                      as_array = False) -> Union[List, np.array]:
        
        """
        builds vectorizer's vocab and then transforms data
        'min_length' defines minimal token's length
        'min_count' defines minimal number of counts for token in 'texts' corpus
        if 'as_array' is True then numpy array of shape (len('texts'), 'num_features') is returned, else list of lists
        """
        
        self.fit(texts, min_count, min_length, ordering)
        
        return self.transform(texts, as_array)
        
    def transform(self, texts: List[str], as_array = False) -> Union[List, np.array]:
        
        """
        transforms data using earlier built vocab
        if 'as_array' is True then numpy array of shape (len('texts'), 'num_features') is returned, else list of lists
        """
        
        tokenized_texts = self.tokenizer.texts_to_sequences(texts)
        
        L = len(tokenized_texts)
        
        vec = [[0] * self.vocab_size for _ in range(L)]
        
        for i, tokens in enumerate(tokenized_texts):
            
            for token in tokens:
                
                feature_ix = self.stoi(token)
                
                if feature_ix is not None:
                    
                    vec[i][feature_ix] += 1
        
        if as_array:
            
            return np.array(vec)
        
        else:
            
            return vec
            
    def get_feature_names(self):
        
        if self._feature_names is not None:
            
            return self._feature_names
        
        else:
            
            raise AttributeError('vectorizer is not fitted yet - need to fit first')
            
            
class TfIdfVectorizer(CountVectorizer):
    
    def __init__(self, tokenizer, max_features = None):
        
        super().__init__(tokenizer, max_features)
        self.tfidf_transformer = TfidfTransformer()
        
    def fit(self, texts: List[str], min_count = 1, min_length = 1, ordering = 'counts'):
        
        super(TfIdfVectorizer, self).fit(texts, min_count, min_length, ordering)
        count_matrix = super(TfIdfVectorizer, self).transform(texts, as_array)
        
        self.tfidf_transformer.fit(count_matrix)
        
    def transform(self, texts: List[str], as_array = False):
        
        count_matrix = super(TfIdfVectorizer, self).transform(texts, as_array)
        return self.tfidf_transformer.transform(count_matrix)
        
    def fit_transform(self, texts: List[str], min_count = 1, min_length = 1, ordering = 'counts',
                      as_array = False) -> Union[List, np.array]:
        
        #count_matrix = super(TfIdfVectorizer, self).fit_transform(texts, min_count, min_length, ordering, as_array)
        ### тут будет проблема, потому что в fit_transform дергается внутри метод self.fit, который уже перегружен
        ### здесь для TfIdfVectorizer, а хотелось бы именно родительского класса, поэтому разнесём на два метода
        
        super(TfIdfVectorizer, self).fit(texts, min_count, min_length, ordering)
        count_matrix = super(TfIdfVectorizer, self).transform(texts, as_array)
        
        return self.tfidf_transformer.fit_transform(count_matrix)
