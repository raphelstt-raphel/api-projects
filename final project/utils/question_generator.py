import spacy
import random
import re

# Load English tokenizer, tagger, parser and NER
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

def generate_questions(text, question_types):
    """
    Generates questions based on the text and selected types.
    """
    doc = nlp(text)
    questions = {}

    if 'mcq' in question_types:
        questions['MCQs'] = generate_mcqs(doc)
    
    if '5_mark' in question_types:
        questions['Short Answer Questions (5 Marks)'] = generate_short_questions(doc)
        
    if '8_mark' in question_types:
        questions['Long Answer Questions (8 Marks)'] = generate_long_questions(doc)
        
    return questions

def generate_mcqs(doc):
    mcqs = []
    # Identify definition sentences: "Subject is Definition"
    for sent in doc.sents:
        sent_text = sent.text.strip()
        if len(sent_text.split()) < 5 or len(sent_text.split()) > 30: # Constraint length
            continue
            
        # Analyze syntax
        # Looking for simple format: NOUN AUX ...
        # e.g., "Python is a programming language."
        
        # very simple heuristic: split by " is " or " are "
        if " is a " in sent_text or " is an " in sent_text:
            parts = re.split(r"\s+is\s+(?:a|an)\s+", sent_text, 1)
            if len(parts) == 2:
                subject = parts[0].strip()
                rest = parts[1].strip()
                
                # Check if subject is noun-phrase like
                # Generate distractors from other nouns in the document
                distractors = get_distractors(doc, subject)
                
                if len(distractors) >= 2:
                    options = [subject] + distractors[:3]
                    random.shuffle(options)
                    
                    question = {
                        "question": f"__________ is {rest}",
                        "options": options,
                        "answer": subject
                    }
                    mcqs.append(question)
                    
        if len(mcqs) >= 10: # limit to 10 MCQs
            break
            
    return mcqs

def get_distractors(doc, correct_answer):
    distractors = set()
    for token in doc:
        if token.pos_ == "PROPN" or token.pos_ == "NOUN":
            word = token.text
            if word.lower() != correct_answer.lower() and len(word) > 2:
                distractors.add(word)
        if len(distractors) >= 10:
            break
    return list(distractors)

def generate_short_questions(doc):
    questions = []
    # 5 marks: Processes, Steps, Methods
    keywords = ["process", "step", "method", "algorithm", "technique", "mechanism"]
    
    seen_questions = set()

    for sent in doc.sents:
        sent_text = sent.text.strip()
        
        for kw in keywords:
            if kw in sent_text.lower():
                # Extract the noun phrase containing the keyword
                # Simplified: matches "process of X" or "X algorithm"
                if f"{kw} of" in sent_text.lower():
                     # try to grab what it is a process of
                     match = re.search(r'\b'+kw+r'\s+of\s+([a-zA-Z\s]+)', sent_text, re.IGNORECASE)
                     if match:
                         topic = match.group(1).strip()
                         q = f"Explain the {kw} of {topic}."
                         if q not in seen_questions:
                             questions.append(q)
                             seen_questions.add(q)
                
                elif f"{kw} for" in sent_text.lower():
                     match = re.search(r'\b'+kw+r'\s+for\s+([a-zA-Z\s]+)', sent_text, re.IGNORECASE)
                     if match:
                         topic = match.group(1).strip()
                         q = f"Describe the {kw} for {topic}."
                         if q not in seen_questions:
                             questions.append(q)
                             seen_questions.add(q)
    
    return unique_questions(questions)

def generate_long_questions(doc):
    questions = []
    # 8 marks: Types, Advantages, Importance, Features, Characteristics, Architecture
    keywords = ["types", "advantages", "disadvantages", "importance", "features", "characteristics", "benefits", "architecture", "components"]
    
    seen_questions = set()
    
    for sent in doc.sents:
        sent_text = sent.text.strip()
        
        for kw in keywords:
            if kw in sent_text.lower():
                 # "Types of X", "Advantages of X"
                 if f"{kw} of" in sent_text.lower():
                     match = re.search(r'\b'+kw+r'\s+of\s+([a-zA-Z\s]+)', sent_text, re.IGNORECASE)
                     if match:
                         topic = match.group(1).strip()
                         q = f"Discuss the {kw} of {topic} in detail."
                         if q not in seen_questions:
                             questions.append(q)
                             seen_questions.add(q)
    
    return unique_questions(questions)

def unique_questions(questions):
    # remove duplicates and limit to reasonable amount
    # Filter extremely long or short junk
    clean_q = []
    for q in questions:
        if len(q) < 100: # not too long
            clean_q.append(q)
    return list(set(clean_q))[:8] # limit
