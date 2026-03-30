state = {'loaded': False}

def handle_upload(file, num_q):
    if file is None:
        return ('<p style="color:#ef4444;">Please upload a document first.</p>',
                gr.update(visible=False), gr.update(visible=False),
                gr.update(visible=False), '', gr.update(visible=False))
    try:
        n = session.load_document(file.name, num_questions=int(num_q))
        state['loaded'] = True
        item = session.current_question()
        return (q_html(item, 1, n), gr.update(visible=True), gr.update(visible=True),
                gr.update(visible=False), '', gr.update(visible=False))
    except Exception as e:
        return (f'<p style="color:#ef4444;">Error: {str(e)}</p>',
                gr.update(visible=False), gr.update(visible=False),
                gr.update(visible=False), '', gr.update(visible=False))

def handle_submit(ua):
    if not state.get('loaded'):
        return ('<p style="color:#f59e0b;">Upload a document first.</p>',
                gr.update(visible=False), gr.update(visible=False),
                gr.update(visible=False), '', gr.update(visible=False))
    if not ua.strip():
        return ('<p style="color:#f59e0b;">Please enter an answer first.</p>',
                gr.update(visible=True), gr.update(visible=True),
                gr.update(visible=False), ua, gr.update(visible=False))
    result = session.submit_answer(ua)
    rh = r_html(result)
    if session.is_complete():
        return (rh, gr.update(visible=False), gr.update(visible=False),
                gr.update(visible=True), '', gr.update(visible=True, value='See Final Summary'))
    return (rh, gr.update(visible=False), gr.update(visible=False),
            gr.update(visible=True), '', gr.update(visible=True, value='Next Question'))

def handle_next(btn_lbl):
    if 'Summary' in str(btn_lbl) or session.is_complete():
        sm = session.summary()
        return ('', gr.update(visible=False), gr.update(visible=False),
                gr.update(visible=False), '', gr.update(visible=False),
                gr.update(visible=True, value=s_html(sm)))
    item = session.current_question()
    qn = session.current_index + 1
    total = len(session.quiz_items)
    return (q_html(item, qn, total), gr.update(visible=True), gr.update(visible=True),
            gr.update(visible=False), '', gr.update(visible=False), gr.update(visible=False))

def handle_restart():
    session.reset()
    state['loaded'] = False
    return ('<p style="color:#64748b;text-align:center;padding:40px;">Upload a document to begin.</p>',
            gr.update(visible=False), gr.update(visible=False),
            gr.update(visible=False), '', gr.update(visible=False),
            gr.update(visible=False, value=''))

def export_handler():
    df = session.export_results()
    path = '/content/quiz_results.csv'
    df.to_csv(path, index=False)
    return f'Exported {len(df)} results to quiz_results.csv', gr.update(visible=True, value=path)
