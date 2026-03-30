import gradio as gr
from modules.document_ingester import DocumentIngester
from modules.question_generator import QuestionGenerator
from modules.answer_evaluator import AnswerEvaluator
from modules.quiz_session import QuizSession
from sentence_transformers import SentenceTransformer
from utils.handlers import *
from utils.html_templates import *
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load models
tokenizer = AutoTokenizer.from_pretrained('mrm8488/t5-base-finetuned-question-generation-ap')
model = AutoModelForSeq2SeqLM.from_pretrained('mrm8488/t5-base-finetuned-question-generation-ap')

def custom_qg_pipeline(inputs, max_length=128, num_beams=4, device=-1):
    input_ids = tokenizer(inputs, return_tensors='pt', padding=True, truncation=True).input_ids
    outputs = model.generate(input_ids, max_length=max_length, num_beams=num_beams, early_stopping=True)
    return [{'generated_text': tokenizer.decode(outputs[0], skip_special_tokens=True)}]

embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize modules
ingester = DocumentIngester()
qgen = QuestionGenerator(custom_qg_pipeline)
evaluator = AnswerEvaluator(embed_model)
session = QuizSession(ingester, qgen, evaluator)

# GRADIO UI CODE 
HEADER = '''
<div style="background-color: #1a1a1a; border: 1px solid #333; border-radius: 12px; padding: 24px; text-align: center; margin-bottom: 16px;">
    <div style="font-size: 2.2rem; font-weight: 700; color: #00bcd4; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        AI QuizMaster
    </div>
    <p style="color: #bbb; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 8px 0 16px;">
        Upload your document, get AI-generated questions, and evaluate your answers with smart scoring.
    </p>
    <div style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;">
        <span style="background-color: #2a2a2a; border: 1px solid #444; padding: 4px 10px; border-radius: 16px; color: #00bcd4; font-size: 0.75rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Multi-Format Docs</span>
        <span style="background-color: #2a2a2a; border: 1px solid #444; padding: 4px 10px; border-radius: 16px; color: #00bcd4; font-size: 0.75rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">T5 Question Gen</span>
        <span style="background-color: #2a2a2a; border: 1px solid #444; padding: 4px 10px; border-radius: 16px; color: #00bcd4; font-size: 0.75rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Semantic Scoring</span>
        <span style="background-color: #2a2a2a; border: 1px solid #444; padding: 4px 10px; border-radius: 16px; color: #00bcd4; font-size: 0.75rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Open Source Stack</span>
    </div>
</div>
'''

HOW = '''
<div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 0.8rem; color: #999; margin-top: 16px; padding: 10px; border-radius: 8px; background-color: #1a1a1a;">
    <p style="font-weight: 600; color: #00bcd4; margin-bottom: 8px;">HOW IT WORKS</p>
    <ul style="list-style-type: disc; padding-left: 20px; margin: 0;">
        <li style="margin-bottom: 5px;">Upload your study document (PDF, TXT, DOCX).</li>
        <li style="margin-bottom: 5px;">AI intelligently generates questions from your content.</li>
        <li style="margin-bottom: 5px;">Type your answers in the provided box.</li>
        <li style="margin-bottom: 5px;">LLM evaluates your response using advanced semantic matching.</li>
        <li style="margin-bottom: 5px;">Receive detailed, per-question feedback.</li>
        <li>Review your overall performance and export a CSV report.</li>
    </ul>
</div>
'''

INIT = '<p style="color: #aaa; text-align: center; padding: 50px; font-family: \'Segoe UI\', Tahoma, Geneva, Verdana, sans-serif; font-size: 1.1rem;">Ready to learn? Upload a document and click "Generate Quiz" to begin.</p>'

with gr.Blocks(title='AI Quiz App') as app:
    gr.HTML(HEADER)

    with gr.Row():
        with gr.Column(scale=1):
            gr.HTML('<h3 style="color:#00bcd4;font-family:\'Segoe UI\', Tahoma, Geneva, Verdana, sans-serif;">Document Setup</h3>')
            file_input = gr.File(label='Upload (PDF / TXT / DOCX)', file_types=['.pdf','.txt','.docx'])
            num_q = gr.Slider(minimum=3, maximum=10, value=5, step=1, label='Number of Questions')
            upload_btn  = gr.Button('Generate Quiz', variant='primary')
            restart_btn = gr.Button('Start Over', variant='secondary')
            gr.HTML(HOW)

        with gr.Column(scale=2):
            question_html = gr.HTML(value=INIT)
            answer_box     = gr.Textbox(label='Your Answer', placeholder='Type your answer here...', lines=4, visible=False)
            submit_btn    = gr.Button('Submit Answer', variant='primary', visible=False)
            result_html   = gr.HTML(visible=False)
            next_btn      = gr.Button('Next Question', variant='primary', visible=False)

    summary_html = gr.HTML(visible=False)

    with gr.Row():
        export_btn    = gr.Button('Export Results as CSV')
        export_status = gr.Textbox(label='Export Status', interactive=False)

    export_file = gr.File(label='Download Results', visible=False)

    upload_btn.click(
        fn=handle_upload, inputs=[file_input, num_q],
        outputs=[question_html, answer_box, submit_btn, result_html, answer_box, next_btn])

    submit_btn.click(
        fn=handle_submit, inputs=[answer_box],
        outputs=[result_html, answer_box, submit_btn, result_html, answer_box, next_btn])

    next_btn.click(
        fn=handle_next, inputs=[next_btn],
        outputs=[question_html, answer_box, submit_btn, result_html, answer_box, next_btn, summary_html])

    restart_btn.click(
        fn=handle_restart, inputs=[],
        outputs=[question_html, answer_box, submit_btn, result_html, answer_box, next_btn, summary_html])

    export_btn.click(
        fn=export_handler, inputs=[], outputs=[export_status, export_file])

app.launch(share=True, debug=False)
