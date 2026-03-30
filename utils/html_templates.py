def q_html(item, q_num, total):
    pct = int((q_num-1)/total*100)
    qtext = item['question']
    ctx = item['context'][:250]
    return f"""
    <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #eee; background-color: #1e1e1e; padding: 20px; border-radius: 12px; border: 1px solid #333;">
        <div style="display:flex;justify-content:space-between;margin-bottom:10px; align-items: center;">
            <span style="color:#00bcd4;font-weight:700; font-size: 1.1rem;">QUESTION {q_num} of {total}</span>
            <span style="color:#666; font-size: 0.9rem;">{pct}% complete</span>
        </div>
        <div style="background:#333;border-radius:4px;height:6px;margin-bottom:16px;">
            <div style="background:linear-gradient(90deg,#00bcd4,#00e676);height:100%;width:{pct}%;border-radius:4px;"></div>
        </div>
        <div style="background-color:#2a2a2a; border:1px solid #444; border-radius:10px; padding:18px; margin-bottom:16px;">
            <p style="font-size:1.15rem;font-weight:600;color:#f1f1f1;margin:0;">{qtext}</p>
        </div>
        <div style="border-left:4px solid #00bcd4; padding:10px 15px; background-color:#252525; border-radius:0 8px 8px 0;">
            <p style="font-size:0.75rem;color:#999;margin:0 0 5px 0;font-weight:700;">CONTEXT HINT</p>
            <p style="font-size:0.85rem;color:#ccc;margin:0;">{ctx}...</p>
        </div>
    </div>
    """

def r_html(r):
    return f"""
    <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #eee; background-color: #1e1e1e; padding: 20px; border-radius: 12px; border: 1px solid #333;">
        <div style="display:flex;align-items:center;gap:16px;margin-bottom:20px;">
            <div style="background:linear-gradient(135deg,#00bcd4,#00e676);width:60px;height:60px;
            border-radius:50%;display:flex;align-items:center;justify-content:center;
            font-size:1.5rem;font-weight:800;color:white;">{r['score']}</div>
            <div>
                <div style="font-size:1.2rem;font-weight:700;color:#f1f1f1;">{r['grade']}</div>
                <div style="font-size:0.8rem;color:#888;">out of 10 points</div>
            </div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px;">
            <div style="background-color:#2a2a2a; border:1px solid #444; border-radius:10px; padding:14px;">
                <div style="color:#999;font-size:0.75rem;font-weight:700;">SEMANTIC MATCH</div>
                <div style="font-size:1.3rem;font-weight:700;color:#00bcd4;">{r['semantic_similarity']}%</div>
            </div>
            <div style="background-color:#2a2a2a; border:1px solid #444; border-radius:10px; padding:14px;">
                <div style="color:#999;font-size:0.75rem;font-weight:700;">KEYWORD MATCH</div>
                <div style="font-size:1.3rem;font-weight:700;color:#00e676;">{r['keyword_overlap']}%</div>
            </div>
        </div>
        <div style="background-color:#252525; border:1px solid #444; border-radius:10px; padding:14px; margin-bottom:12px;">
            <div style="color:#999;font-size:0.75rem;font-weight:700;margin-bottom:8px;">FEEDBACK</div>
            <p style="margin:0;color:#ccc;font-size:0.9rem;">{r['feedback']}</p>
        </div>
        <div style="background-color:#252525; border:1px solid #444; border-radius:10px; padding:14px;">
            <div style="color:#00bcd4;font-size:0.75rem;font-weight:700;margin-bottom:8px;">REFERENCE ANSWER</div>
            <p style="margin:0;color:#ccc;font-size:0.88rem;">{r['reference_answer']}</p>
        </div>
    </div>
    """

def s_html(summary):
    pct = summary['percentage']
    if pct >= 80:   lbl, col = 'Outstanding!', '#00e676'
    elif pct >= 60: lbl, col = 'Well Done!', '#aeea00'
    elif pct >= 40: lbl, col = 'Keep Practicing', '#ffb300'
    else:           lbl, col = 'More Study Needed', '#ff3d00'

    rows_html = ""
    for r in summary['results']:
        gc = r['grade_color']
        rows_html += f"""
            <div style="display:flex;gap:12px;padding:12px 0;border-bottom:1px solid #2a2a2a;align-items:flex-start;">
                <div style="background:{gc}33;color:{col};border:1px solid {gc}55;width:38px;height:38px;
                border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:1rem;">{r['score']}</div>
                <div>
                    <p style="margin:0 0 4px 0;color:#eee;font-size:0.9rem;">{r['question']}</p>
                    <p style="margin:0;color:#999;font-size:0.78rem;">{r['grade']} |
                    Semantic: {r['semantic_similarity']}% | Keywords: {r['keyword_overlap']}%</p>
                </div>
            </div>
            """
    return f"""
    <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;color:#eee;">
        <div style="background-color:#1e1e1e; border:1px solid #333;
        border-radius:12px;padding:28px;text-align:center;margin-bottom:20px;">
            <div style="font-size:3rem;font-weight:800;color:{col};">{pct}%</div>
            <div style="font-size:1.2rem;color:#00bcd4;font-weight:700;margin-top:5px;">{lbl}</div>
            <div style="color:#999;font-size:0.85rem;margin-top:10px;">
                Total Questions: {summary['total_questions']} | Average: {summary['average_score']}/10 |
                Highest: {summary['highest']} | Lowest: {summary['lowest']}
            </div>
        </div>
        <div style="background-color:#1e1e1e;border:1px solid #333;border-radius:12px;padding:20px;">
            <h3 style="margin:0 0 12px 0;font-size:0.9rem;color:#00bcd4;text-transform:uppercase;">DETAILED RESULTS</h3>
            {rows_html}
        </div>
    </div>
    """
