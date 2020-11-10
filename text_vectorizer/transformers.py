from math import log

class TfidfTransformer():
    
    def __init__(self):
        
        self.idf = None
    
    def __tf_transform(self, count_matrix):
        
        """ transforms count matrix into TermFrequency matrix """
    
        return [[w / sum(line) for w in line] for line in count_matrix] 
    
    def tf_transform(self, count_matrix):
    
        out_size = len(count_matrix)
        in_size = len(count_matrix[0])

        tf_matrix = [[0]*in_size for _ in range(out_size)]

        for i in range(out_size):

            s = sum(count_matrix[i])

            for j in range(in_size):

                tf_matrix[i][j] = count_matrix[i][j] / s if s != 0 else count_matrix[i][j]

        return tf_matrix
       

    def idf_transform(self, count_matrix):
        
        """ returns InvertedDocumentFrequency vector based on count matrix """
        
        out_size = len(count_matrix)
        in_size = len(count_matrix[0])

        word_total_counts = [0] * in_size

        for j in range(in_size):

            for i in range(out_size):

                word_total_counts[j] += count_matrix[i][j]

            word_total_counts[j] = log( (out_size + 1) / (word_total_counts[j] + 1) ) + 1

        return word_total_counts
    
    def fit(self, count_matrix):
        
        self.idf = self.idf_transform(count_matrix)
        
    def transform(self, count_matrix):
        
        if self.idf is None:
            
            raise AtributeError('transformer is not fitted yet')
            
        else:
        
            out_size = len(count_matrix)
            in_size = len(count_matrix[0])

            idf = self.idf
            tf = self.tf_transform(count_matrix)

            tf_idf_matrix = [[0] * in_size for _ in range(out_size)]

            for i in range(out_size):

                for j in range(in_size):

                    tf_idf_matrix[i][j] = idf[j] * tf[i][j]

            return tf_idf_matrix
        
    def fit_transform(self, count_matrix):
    
        self.fit(count_matrix)
        
        return self.transform(count_matrix)