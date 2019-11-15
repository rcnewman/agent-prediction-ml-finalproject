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
            all_lines = []
            line = ""
            with open(file) as file:
                for l in file.readlines():
                    if re.search("\w", l) is None:
                        all_lines.append(re.sub("\s+", " ", line.strip()))
                        line = ""
                    else:
                        line += l.strip() + " "
            self.text = []
            for line in all_lines:
                self.text.append(list(nltk.sent_tokenize(line)))
        except Exception as e:
            print("Error: Error opening file.")
            print(e)
            
    def generate_features(self):
        # Generate all features from text.
        self.pos_ner_tags = []
        self.corefs = defaultdict(list)
        nlp = spacy.load("en_core_web_sm")
        neuralcoref.add_to_pipe(nlp)
        
        # Iterate through sentences.
        for par in self.text:
            p = []
            doc = ""
            for sent in par:
                if len(doc) > 0:
                    doc += " "
                doc += sent
                
                # Get pos and ner tags.
                sent = nltk.word_tokenize(sent)
                sent = nltk.pos_tag(sent)
                sent = nltk.chunk.ne_chunk(sent)
                p.append(sent)
            self.pos_ner_tags.append(p)
            
            # Do coreference resolution.
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
d = Document("files/pg375.txt", "Peyton Farquhar", "No One")
print(d.corefs)
d.preds()