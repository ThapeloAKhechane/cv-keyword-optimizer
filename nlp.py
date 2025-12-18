import spacy

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    """
    Extract important keywords from text
    """
    doc = nlp(text.lower())
    keywords = set()

    for token in doc:
        if (
            token.pos_ in ["NOUN", "PROPN", "VERB"]
            and not token.is_stop
            and token.is_alpha
        ):
            keywords.add(token.lemma_)

    return keywords


def compare_cv_to_job(cv_text, job_text):
    """
    Compare CV text with job description
    """
    cv_keywords = extract_keywords(cv_text)
    job_keywords = extract_keywords(job_text)

    if not job_keywords:
        return {
            "match_score": 0,
            "missing_keywords": []
        }

    match_score = int(len(cv_keywords & job_keywords) / len(job_keywords) * 100)
    missing_keywords = list(job_keywords - cv_keywords)

    return {
        "match_score": match_score,
        "missing_keywords": missing_keywords[:20]
    }
