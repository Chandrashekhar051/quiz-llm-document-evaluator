import pandas as pd

class QuizSession:
    def __init__(self, ingester, qgen, evaluator):
        self.ingester = ingester
        self.qgen = qgen
        self.evaluator = evaluator
        self.reset()

    def reset(self):
        self.quiz_items = []
        self.current_index = 0
        self.results = []

    def load_document(self, fp, num_questions=5):
        self.reset()
        text = self.ingester.extract(fp)
        chunks = self.ingester.chunk_text(text)
        if not chunks: raise ValueError('Document too short or unreadable.')
        self.quiz_items = self.qgen.generate_quiz(chunks, n=num_questions)
        return len(self.quiz_items)

    def current_question(self):
        if self.current_index < len(self.quiz_items):
            return self.quiz_items[self.current_index]
        return None

    def submit_answer(self, ua):
        item = self.current_question()
        if not item: return None
        r = self.evaluator.evaluate(ua, item['reference_answer'], item['context'])
        r.update({'question': item['question'], 'user_answer': ua, 'q_num': item['id']})
        self.results.append(r)
        self.current_index += 1
        return r

    def is_complete(self):
        return self.current_index >= len(self.quiz_items)

    def summary(self):
        if not self.results: return {}
        scores = [r['score'] for r in self.results]
        avg = round(sum(scores)/len(scores), 2)
        return {'total_questions': len(self.results), 'average_score': avg,
                'percentage': round(avg*10, 1), 'highest': max(scores),
                'lowest': min(scores), 'results': self.results}

    def export_results(self):
        rows = [{'Q#': r['q_num'], 'Question': r['question'],
                 'Your Answer': r['user_answer'], 'Reference': r['reference_answer'],
                 'Score/10': r['score'], 'Grade': r['grade'],
                 'Semantic%': r['semantic_similarity'], 'Keyword%': r['keyword_overlap'],
                 'Feedback': r['feedback']} for r in self.results]
        return pd.DataFrame(rows)
