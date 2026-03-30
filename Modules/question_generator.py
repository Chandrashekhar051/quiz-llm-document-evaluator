import random
from nltk.tokenize import sent_tokenize

class QuestionGenerator:
    def __init__(self, qg):
        self.qg = qg

    def gen_q(self, answer_text, context):
        inp = 'answer: ' + answer_text + '  context: ' + context
        try:
            r = self.qg(inp, max_length=128, num_beams=4)[0]['generated_text']
            r = r.replace('question:', '').strip()
            if r and r[-1] not in '.?!': r += '?'
            return r
        except:
            return None

    def key_answer(self, chunk):
        sents = sent_tokenize(chunk)
        for s in sents:
            if len(s.split()) > 8: return s
        return sents[0] if sents else chunk[:200]

    def generate_quiz(self, chunks, n=5):
        n = min(n, len(chunks))
        quiz = []
        for i, chunk in enumerate(random.sample(chunks, n)):
            key_ans = self.key_answer(chunk)
            q = self.gen_q(key_ans, chunk)
            if q:
                quiz.append({'id': i+1, 'question': q, 'context': chunk,
                             'reference_answer': key_ans})
        return quiz
