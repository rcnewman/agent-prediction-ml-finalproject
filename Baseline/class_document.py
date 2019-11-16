# Installs and Downloads ------------------------------------------------------
# Note: spaCy installation is version 2.1.0.
import ntpath
import nltk
import spacy
import neuralcoref
import re
from collections import defaultdict
import copy
from nltk.tree import Tree

#nltk.download("popular")

# Document Class --------------------------------------------------------------
class Document():
    # Class variables.
    title = None
    text = None
    protagonist_g = None
    antagonist_g = None
    ner_tags = None
    corefs = None
    tmp = None
    
    def __init__(self, title, file, protagonist, antagonist):
        # Initilize class variables.
        self.title = title
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
        self.ner_tags = set()
        self.corefs = defaultdict(list)
        nlp = spacy.load("en_core_web_sm")
        neuralcoref.add_to_pipe(nlp)
        bad_tags = set()
        
        # Iterate through sentences.
        for par in self.text:
            doc = ""
            for sent in par:
                if len(doc) > 0:
                    doc += " "
                doc += sent
                
                # Get pos and ner tags.
                sent = nltk.word_tokenize(sent)
                sent = nltk.pos_tag(sent)
                sent = nltk.chunk.ne_chunk(sent)
                for chunk in sent:
                    if hasattr(chunk, "label"):
                        if chunk.label() == "PERSON" or chunk.label() == "ORGANIZATION":
                            self.ner_tags.add(self.entitiy_cleaner("".join(c[0] for c in chunk)))
#                        else:
#                            bad_tags.add(("".join(c[0] for c in chunk), chunk.label()))
                if self.tmp is None:
                    self.tmp = sent
            
            # Do coreference resolution.
            crefs = defaultdict(list)
            doc = nlp(doc)
            for ent in doc.ents:
                if ent._.is_coref:
                    key = self.entitiy_cleaner(ent)
                    crefs[key].extend(list(ent._.coref_cluster))
            for k in sorted(crefs, key = len, reverse = True):
                in_c = False
                for n in self.ner_tags:
                    if k in n or n in k:
                        in_c = True
                if in_c == False:
                    continue
                in_c = False
                for k_m in self.corefs.keys():
                    if k in k_m or k_m in k:
                        self.corefs[k_m].extend(crefs[k])
                        in_c = True
                        break
                if in_c == False:
                    self.corefs.update({k: crefs[k]})
        
    def get_people(self, text):
        chunked = nltk.ne_chunk(text)
        continuous_chunk = []
        current_chunk = []
        for i in chunked:
            if type(i) == Tree:
                current_chunk.append(" ".join([token for token, pos in i.leaves()]))
            elif current_chunk:
                named_entity = " ".join(current_chunk)
                if named_entity not in continuous_chunk:
                    continuous_chunk.append(named_entity)
                    current_chunk = []
            else:
                continue
        return continuous_chunk
    
    def entitiy_cleaner(self, ent):
        return re.sub("\s+", " ", str(ent).strip()).lower()
    
    def preds(self):
        from tabulate import tabulate
        cref_keys = sorted(self.corefs, key = lambda k: len(self.corefs[k]), reverse = False)
        for k in self.corefs:
            if "gutenberg" in k:
                del cref_keys[cref_keys.index(k)]
        
        p = cref_keys[-1]
        a = cref_keys[-2]
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