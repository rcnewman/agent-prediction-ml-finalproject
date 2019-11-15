# Installs and Downloads ------------------------------------------------------
# Note: spaCy installation is version 2.1.0.
import ntpath
import nltk
import spacy
import neuralcoref
import re
from collections import defaultdict

#nltk.download("popular")

# Document Class --------------------------------------------------------------
class Document():
    # Class variables.
    title = None
    text = None
    protagonist_g = None
    antagonist_g = None
    pos_ner_tags = None
    corefs = None
    
    def __init__(self, file, protagonist, antagonist):
        # Initilize class variables.
        self.title = ntpath.basename(file).rsplit(".", 1)[-2]
        self.protagonist_g = protagonist
        self.antagonist_g = antagonist
        self.open_file(file)
        self.generate_features()
    
    def open_file(self, file):
        # Open file.
        try:
            lines = ""
            with open(file) as file:
                for l in file.readlines():
                    lines += l.strip() + " "
            self.text = nltk.sent_tokenize(lines)
        except Exception as e:
            print("Error: Error opening file.")
            print(e)
            
    def generate_features(self):
        # Generate all features from text.
        self.pos_ner_tags = []
        doc = ""
        self.corefs = defaultdict(list)
        
        # Iterate through sentences.
        for sent in self.text:
            if len(doc) > 0:
                doc += " "
            doc += sent
            
            # Get pos and ner tags.
            sent = nltk.word_tokenize(sent)
            sent = nltk.pos_tag(sent)
            sent = nltk.chunk.ne_chunk(sent)
            self.pos_ner_tags.append(sent)
            
        # Do coreference resolution.
        nlp = spacy.load("en_core_web_sm")
        neuralcoref.add_to_pipe(nlp)
        doc = nlp(doc)
        for ent in doc.ents:
            if ent._.is_coref:
                key = self.entitiy_cleaner(ent)
                self.corefs[key].extend(ent._.coref_cluster)
            
    
    def entitiy_cleaner(self, ent):
        return re.sub("\s+", " ", str(ent).strip()).lower()
    
    def preds(self):
        from tabulate import tabulate
        p = None
        a = None
        for e in self.corefs:
            if re.search("gutenberg", e) is not None:
                continue
            if p is None:
                p = e
            if len(self.corefs[e]) > len(self.corefs[p]):
                a = p
                p = e
        pg = self.entitiy_cleaner(str(self.protagonist_g))
        if pg in p or p in pg:
            pg = True
        else:
            pg = False
        ag = self.entitiy_cleaner(str(self.antagonist_g))
        if ag in a or a in ag:
            ag = True
        else:
            ag = False
        values = [
                    ["Protagonist", p, self.protagonist_g, pg], 
                    ["Antagonist", a, self.antagonist_g, ag]
                    ]
        print(self.title)
        print(tabulate(values, headers = ["Prediction", "Gold", "Compare"]))
        print()
        return [pg, ag]
            
# Test - Delete 
#d = Document("files/pg375.txt", "Peyton Farquhar", "No One")
#d.preds()