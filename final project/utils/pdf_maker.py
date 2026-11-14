from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT

def create_pdf(questions, output_filename):
    """
    Generates a PDF from the dictionary of questions.
    """
    doc = SimpleDocTemplate(output_filename, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    Story = []
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    
    # Title
    title_style = styles["Heading1"]
    title_style.alignment = TA_LEFT
    Story.append(Paragraph("Generated Questions", title_style))
    Story.append(Spacer(1, 12))
    
    # Iterate through question categories
    for category, q_list in questions.items():
        if not q_list:
            continue
            
        # Category Heading
        Story.append(Paragraph(category, styles["Heading2"]))
        Story.append(Spacer(1, 12))
        
        # Questions
        for i, q in enumerate(q_list, 1):
            if category == 'MCQs':
                # q is a dictionary for MCQs
                text = f"{i}. {q['question']}"
                Story.append(Paragraph(text, styles["Normal"]))
                
                # Options
                for opt in q['options']:
                    Story.append(Paragraph(f"   o {opt}", styles["Normal"]))
                
                # Answer (hidden/appended or just shown? User req says "clearly mention correct answer")
                # We will show it below the options
                ans_text = f"<b>Correct Answer: {q['answer']}</b>"
                Story.append(Paragraph(ans_text, styles["Normal"]))
                Story.append(Spacer(1, 12))
                
            else:
                # Text questions
                text = f"{i}. {q}"
                Story.append(Paragraph(text, styles["Normal"]))
                Story.append(Spacer(1, 12))
        
        Story.append(Spacer(1, 24))
        
    doc.build(Story)
    return output_filename
