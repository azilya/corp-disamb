#/usr/bin/python3
# -!- enc: utf-8 -!-

import ast, random, re

folder=input("Folder: ")
corpus = open(folder+"/ruscorp.csv").read().split("\n")
mystems = open(folder+"/mystem.csv").read().split("\n")
freeling = open(folder+"/freeling.csv").read().split("\n")

gloss = [
    {"S":1, "A":2, "V":3, "SPRO":4, "APRO":5, "ADV":6, "CONJ":7, "PART":8, "PR":9, "INTJ":10, "NUM":11},
    {"им":1, "вин":2, "род":3, "твор":4, "пр":5, "дат":6},
    {"ед":1, "мн":2},
    {"муж":1, "жен":2, "сред":3},
    {"прош":1, "непрош":2},
    {"1-л":1, "2-л":2, "3-л":3, "инф":4, "прич":5}
]

lines = list(range(len(corpus)))
random.seed(int(input("Seed: ")))
random.shuffle(lines)
char=

def analyze_sum(pos, gram):
    morph = [0]
    for a in sorted(gloss[0].keys()):
        if a in pos: morph[0] += gloss[0][a] # for sums
        
    for i in range(0,6):
        morph.insert(i, 0)
        for a in gloss[i]:
            if a in gram: morph[i] += gloss[i][a] # for sums
    return morph
    
def extend_sum():
    cont = []
    for a in [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]:
        _morph = [0]
        if i+a in lines:
            _cont = ast.literal_eval(corpus[i+a].replace(",[", ";[").replace("],", "];").split(";")[1])
            c_pos = set([re.search("[A-Z]+", a['gr']).group() for a in _cont])
            for a in gloss[0]:
                if a in c_pos: _morph[0] += gloss[0][a]
            c_gram = [re.search("(?<==)[а-я,]*", a['gr']).group() for a in _cont]
            for i in range(1,6):
                _morph.insert(i, 0)
                for a in gloss[i]:
                    if a in gram: _morph[i] += gloss[i][a]
            cont.extend(_morph)
    return cont        

def analyze_char(pos, gram):
    morph = []
    for a in sorted(gloss[0].keys()):
        if a in pos:  
            morph.append(1)
        else: morph.append(0
    for i in range(1,6):
        for a in sorted(gloss[0].keys()):
            if a in gram:
                morph.append(1)
            else: morph.append(0)
    return morph
    
def extend_char(morph):
    cont = []
    for a in [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]:
        _morph = [0]
        if i+a in lines:
            _cont = ast.literal_eval(corpus[i+a].replace(",[", ";[").replace("],", "];").split(";")[1])
            c_pos = set([re.search("[A-Z]+", a['gr']).group() for a in _cont])
            for a in sorted(gloss[0].keys()):
                if a in pos:
                    morph.extend([1])
                else: morph.extend([0])
            c_gram = [re.search("(?<==)[а-я,]*", a['gr']).group() for a in _cont]
            for i in range(1,6):
                for a in sorted(gloss[0].keys()):
                    if a in gram:
                        morph.extend([1])
                    else: morph.extend([0])
            cont.extend(_morph)
    return cont    
    
def prepare(i, char):
    # char = True ## uncomment to create a dataset of characteristic functions
    corp = corpus[i]
    if corp:
        form = corp.split(",")[0]
        lemma = corp.split(",")[1]
    frl = freeling[i]
    if frl:
        frl_lemma = frl.split(",")[0]
    mslem = mystems[i].split(',')[0]
    out = []

    pos = [re.search("[A-Z]+", a['gr']).group() for a in rusmor]
    if (len(set(pos)) < 2) or not (("A" in pos or "V" in pos) and "S" in pos): return None #for reasons behind this, refer to my research paper
    lem = 0
    for item in rusmor:
        if item['lex'] == lemma.strip("?"):
            lem = gloss[0][re.search("[A-Z]+", item['gr']).group()]
    gram = [re.search("(?<==)[а-я,]*", a['gr']).group() for a in rusmor]
    
    if char: 
        morph = analyze_char(pos, gram)
        morph += extend_char(morph)
    else: 
        morph = analyze_sum(pos, gram)
        morph = extend_sum(morph)
 
    if lemma.strip("?") == mslem and lemma.strip("?") == frl_lemma: pass
    else:
        out.extend([lem] + morph)
        return out

if __name__ == "__main__":
    train_size = 500
    test_size = 0 #use this to create a separate test dataset
    with open(folder+"-train.csv", 'w', encoding='utf8') as trainset:
        for i in lines[:train_size]:
            item = prepare(i)
            if item:        
                trainset.write(str(item[0])[1:-1]+'\n')
    if test_size > 0:
        with open(folder+"-test.csv", 'w', encoding='utf8') as testset:
            for i in lines[train_size:test_size]:
                item = prepare(i)
                if item:        
                    testset.write(str(item[0])[1:-1]+'\n')
