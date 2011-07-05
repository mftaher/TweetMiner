import stemmer

__source = True
try:
    from lxml import html
    
except:
    print "Error: Requires lxml library from http://lxml.de// for parsing tweet source. Have you installed lxml?"
    __source = False
    pass
#http://www.scipy.org/
try:
    from numpy import dot
    from numpy.linalg import norm
except:
    print "Error: Requires numpy from http://www.scipy.org/. Have you installed scipy?"
    pass
    
def parse_alink(source):
    if __source:
        source = html.fromstring(source).text_content()
        return source
    return "N/A"
def clean(string):
    """ remove any nasty grammar tokens from string """
    string = string.replace(".","")
    string = string.replace(","," ")
    string = string.replace("\"","'")
    string = string.replace("\s+"," ")
    string = string.lower()
    return string
    
def remove_duplicates(list):
	""" remove duplicates from a list """
	return set((item for item in list))
    
def remove_non_ascii(s):
        return "".join(i for i in s if ord(i)<128)
    
def tokenise(string):
    """ break string up into tokens and stem words """
    words = string.split(" ")
    return words

""" Porter Stemming """
def stem_words(filteredText):
    stem = stemmer.Stemmer('english')
    keywords = []
    word = ""
    for token in filteredText:
        if not token.isdigit():
            if len(token) > 2:
                if token.isalpha():
                    st = stem.stemWord(token)
                    word += st.lower()
                if word:
                    keywords.append(word)
                    word = ""
    return keywords
#""" Tokenize tweet text """
#def tokenize(self,text):
#    tokens = []
#    r = re.compile(r"\w+")
#    tokens = re.findall(r,text);
#    return tokens

def clean(string):
    """ remove any nasty grammar tokens from string """
    string = string.replace(".","")
    string = string.replace("\s+"," ")
    string = string.lower()
    return string
    
def cosine(vector1, vector2):
    """ related documents j and q are in the concept space by comparing the vectors :
            cosine  = ( V1 * V2 ) / ||V1|| x ||V2|| """
    return float(dot(vector1,vector2) / (norm(vector1) * norm(vector2)))

def euclidean(vector1,vector2):
    """ Computes the Euclidean distance between two n-vectors V1 and V2, ||V1-V2||_2 """
    return float(norm(vector1-vector2))