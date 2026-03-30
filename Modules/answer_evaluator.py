import re
from sentence_transformers import util

class AnswerEvaluator:
    def __init__(self, model):
        self.model = model

    def sem_score(self, ua, ra):
        if not ua.strip(): return 0.0
        eu = self.model.encode(ua, convert_to_tensor=True)
        er = self.model.encode(ra, convert_to_tensor=True)
        return max(0.0, util.cos_sim(eu, er).item())

    def kw_score(self, ua, ra):
        if not ua.strip(): return 0.0
        stop = {'the','a','an','is','are','was','were','to','of','and',
                'in','it','that','this','with','for','on','at','by','from'}
        ref = set(w.lower() for w in re.findall(r'\b\w+\b', ra)
                  if w.lower() not in stop and len(w) > 3)
        usr = set(w.lower() for w in re.findall(r'\b\w+\b', ua))
        return len(ref & usr) / len(ref) if ref else 0.5

    def evaluate(self, ua, ra, ctx):
        sem = self.sem_score(ua, ra)
        kw  = self.kw_score(ua, ra)
        score = round((sem * 0.65 + kw * 0.35) * 10, 2)
        if score >= 8:   grade, color = 'Excellent', '#22c55e'
        elif score >= 6: grade, color = 'Good', '#84cc16'
        elif score >= 4: grade, color = 'Partial', '#f59e0b'
        else:            grade, color = 'Needs Improvement', '#ef4444'
        if sem < 0.3:          tip = 'Off-topic. Re-read the context carefully.'
        elif kw < 0.3:         tip = 'Right direction but missing key terms.'
        elif sem >= 0.7:       tip = 'Excellent! Captures both meaning and key concepts.'
        else:                  tip = 'Good understanding. Try to be more specific.'
        return {'score': score, 'grade': grade, 'grade_color': color,
                'semantic_similarity': round(sem*100, 1),
                'keyword_overlap': round(kw*100, 1),
                'feedback': tip, 'reference_answer': ra}
