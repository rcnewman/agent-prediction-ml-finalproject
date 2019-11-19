# Installs and Downloads ------------------------------------------------------
# Note: spaCy installation is version 2.1.0.
import nltk
import spacy
import neuralcoref
import re
from collections import defaultdict
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from tabulate import tabulate
import numpy as np

#nltk.download("popular")
#nltk.downoad("vader_lexicon")

# Document Class --------------------------------------------------------------
class Document():
    # Class variables.
    title = None
    text = None
    protagonist_g = None
    antagonist_g = None
    ner_tags = None
    sentiments = None
    corefs = None
    
    def __init__(self, title, file, protagonist, antagonist):
        # Initilize class variables.
        self.title = title
        self.protagonist_g = self.entitiy_cleaner(protagonist)
        self.antagonist_g = self.entitiy_cleaner(antagonist)
        self.open_file(file)
        self.generate_features()
    
    def open_file(self, file):
        # Open file.
        try:
            all_lines = []
            line = ""
            with open(file) as file:
                header_end = False
                for l in file.readlines():
                    if "*** END OF THIS PROJECT GUTENBERG EBOOK" in l:
                        break
                    if "*** START OF THIS PROJECT GUTENBERG EBOOK" in l:
                        header_end = True
                    if header_end == False:
                        continue
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
        self.sentiments = {}
        self.corefs = defaultdict(int)
        nlp = spacy.load("en_core_web_sm")
        neuralcoref.add_to_pipe(nlp)
        
        # Iterate through sentences.
        for par in self.text:
            doc = ""
            for sent in par:
                if len(doc) > 0:
                    doc += " "
                doc += sent
                
                # Get pos and ner tags.
                tokens = nltk.word_tokenize(sent)
                tokens = nltk.pos_tag(tokens)
                tokens = nltk.chunk.ne_chunk(tokens)
                for chunk in tokens:
                    if hasattr(chunk, "label"):
                        if chunk.label() == "PERSON" or chunk.label() == "ORGANIZATION":
                            ent = self.entitiy_cleaner("".join(c[0] for c in chunk))
                            self.ner_tags.add(ent)
                            if ent not in self.sentiments:
                                self.sentiments.update({ent: []})
                            self.sentiments[ent].append(sent)
            
            # Do coreference resolution.
            crefs = defaultdict(int)
            doc = nlp(doc)
            for ent in doc.ents:
                key = self.entitiy_cleaner(ent)
                if ent._.is_coref:
                    crefs[key] += len(list(ent._.coref_cluster))
                else:
                    crefs[key] += 1
            for k in sorted(crefs, key = len, reverse = True):
                in_c = False
                for n in self.ner_tags:
                    if k in n or n in k:
                        in_c = True
                if in_c == False:
                    continue
                in_c = False
                for k_m in crefs:
                    if k in k_m:
                        self.corefs[k_m] += crefs[k]/2
                        in_c = True
                        break
                    if k_m in k:
                        self.corefs[k] += crefs[k_m]/2
                        in_c = True
                        break
                if in_c == False:
                    self.corefs[k] += 1
        total = 0.0
        for ent in self.corefs:
            total += self.corefs[ent]
        for ent in self.corefs:
            self.corefs[ent] = self.corefs[ent]/total
        
        # Do sentiment analysis.
        sid = SentimentIntensityAnalyzer()
        for ent in self.sentiments:
            s = 0
            for sent in self.sentiments[ent]:
#                print(sid.polarity_scores(sent))
                s += sid.polarity_scores(sent)["compound"]
            self.sentiments[ent] = s/len(self.sentiments[ent])
    
    def entitiy_cleaner(self, ent):
        return re.sub("\s+", " ", str(ent).strip()).lower()
    
    def get_features(self):
        features = []
        for ent in self.ner_tags:
            if ent not in self.sentiments or ent not in self.corefs:
                continue
            features.append([str(ent), self.corefs[ent], self.sentiments[ent]])
        return features
    
    def get_gold_labels(self):
        labels = []
        for ent in self.ner_tags:
            if ent not in self.sentiments or ent not in self.corefs:
                continue
            label = ""
            if ent in self.protagonist_g or self.protagonist_g in ent:
                label = "p"
            elif ent in self.antagonist_g or self.antagonist_g in ent:
                label = "a"
            else:
                label = "n"
            labels.append(label)
        return labels
    
    def preds(self):
        cref_keys = sorted(self.corefs, key = lambda k: len(self.corefs[k]), reverse = False)
        for k in self.corefs:
            if "gutenberg" in k:
                del cref_keys[cref_keys.index(k)]
        
        p = cref_keys[-1]
        a = cref_keys[-2]
        pg = self.protagonist_g
        if pg in p or p in pg:
            pg = True
        else:
            pg = False
        ag = self.antagonist_g
        if ag in a or a in ag:
            ag = True
        else:
            ag = False
        values = [
                    ["Protagonist", p, self.protagonist_g, pg], 
                    ["Antagonist", a, self.antagonist_g, ag]
                    ]
        print(self.title)
#        print(tabulate(values, headers = ["Prediction", "Gold", "Compare"]))

        return [pg, ag]
    
## TEst
#d = Document("The Monkey's Paw", "../Files/pg12122.txt", "Herbert White", "Sergeant-Major Morris")
#print(d.sentiments)
#print()
#print(d.corefs)

#nlp = spacy.load('en_core_web_sm')
#neuralcoref.add_to_pipe(nlp)
#doc1 = nlp('My sister has a dog.')
#print(doc1._.coref_clusters)
#
#for ent in doc1.ents:
#    print(ent._.coref_cluster)
