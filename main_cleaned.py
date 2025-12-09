from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json
from pathlib import Path

app = FastAPI()

# dizionario che contiene tutti i quiz caricati
quizzes = {}
alt_quizzes = {}  # Nuovo dizionario per quiz alternativi

def load_data():
    """
    Carica i file ordered_questions1.json ... ordered_questions10.json
    """
    global quizzes
    quizzes.clear()
    # MODIFICA QUI: da range(1, 6) a range(1, 11) per includere fino al 10
    for i in range(1, 11): 
        path = Path(f"ordered_questions{i}.json")
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                quizzes[i] = json.load(f)
        else:
            print(f"Attenzione: {path} non trovato.") # Opzionale: per debug
def load_alt_data():
    """
    Carica i file ordered_alt_questions1.json ... ordered_alt_questions5.json
    """
    global alt_quizzes
    alt_quizzes.clear()
    for i in range(1, 6):
        path = Path(f"ordered_alt_questions{i}.json")
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                alt_quizzes[i] = json.load(f)

# carico subito i dati all'avvio
load_data()
load_alt_data()

@app.get("/quiz/{quiz_id}/{index}")
def get_quiz_question(quiz_id: int, index: int):
    """
    Restituisce la domanda 'index' del quiz 'quiz_id'
    """
    if quiz_id not in quizzes:
        return {"errore": "Quiz non trovato"}
    if 0 <= index < len(quizzes[quiz_id]):
        return quizzes[quiz_id][index]
    return {"errore": "Indice non valido"}

@app.get("/quiz_all/{quiz_id}")
def get_quiz_all(quiz_id: int):
    """
    Restituisce tutte le domande di un quiz
    """
    if quiz_id not in quizzes:
        return {"errore": "Quiz non trovato"}
    return quizzes[quiz_id]

# --- ENDPOINT QUIZ ALTERNATIVI ---
@app.get("/quiz_alt/{quiz_id}/{index}")
def get_alt_question(quiz_id: int, index: int):
    """
    Restituisce la domanda 'index' del quiz alternativo 'quiz_id'
    """
    if quiz_id not in alt_quizzes:
        return {"errore": "Quiz alternativo non trovato"}
    if 0 <= index < len(alt_quizzes[quiz_id]):
        return alt_quizzes[quiz_id][index]
    return {"errore": "Indice non valido"}

@app.get("/quiz_all_alt/{quiz_id}")
def get_alt_all(quiz_id: int):
    """
    Restituisce tutte le domande di un quiz alternativo
    """
    if quiz_id not in alt_quizzes:
        return {"errore": "Quiz alternativo non trovato"}
    return alt_quizzes[quiz_id]

@app.get("/", response_class=HTMLResponse)
def index():
    """
    Restituisce la pagina HTML del quiz
    """
    with open("template.html", encoding="utf-8") as f:
        return f.read()
