import re, random, math, textwrap
from collections import defaultdict, deque, Counter


class Informativity:
    @staticmethod
    def tokenize(inp, tokenizer):
        for line in inp:
            for token in tokenizer(line.lower().strip()):
                yield token

    def chars(self, inp):
        return self.tokenize(inp, lambda s: s + " ")

    def words(self, inp):
        return self.tokenize(inp, lambda s: re.findall(r"[a-zA-Z']+", s))

    @staticmethod
    def markov_model(stream, model_order):
        model, stats = defaultdict(Counter), Counter()
        circular_buffer = deque(maxlen=model_order)

        for token in stream:
            prefix = tuple(circular_buffer)
            circular_buffer.append(token)
            if len(prefix) == model_order:
                stats[prefix] += 1
                model[prefix][token] += 1
        return model, stats

    @staticmethod
    def entropy(stats, normalization_factor):
        return -sum(proba / normalization_factor * math.log2(proba / normalization_factor) for proba in stats.values())


#infor = Informativity()
#totalEntropy = 0
#text = ('This is because most methods do some work with the object theyre called on, so there needs to be some way for'
#        'that object to be referred to inside the method. By convention, this first argument is called self inside the '
#        'method definition:')
#model, stats = infor.markov_model(infor.chars(text), 3)
#for prefix in stats:
#    totalEntropy = totalEntropy + infor.entropy(stats, stats[prefix])