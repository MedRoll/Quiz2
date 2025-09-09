from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json
from pathlib import Path

app = FastAPI()

# dizionario che contiene tutti i quiz caricati
quizzes = {}

def load_data():
    """
    Carica i file ordered_questions1.json ... ordered_questions5.json
    """
    global quizzes
    quizzes.clear()
    for i in range(1, 6):
        path = Path(f"ordered_questions{i}.json")
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                quizzes[i] = json.load(f)

# carico subito i dati all'avvio
load_data()

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

@app.get("/", response_class=HTMLResponse)
def index():
    """
    Restituisce la pagina HTML del quiz
    """
    with open("template.html", encoding="utf-8") as f:
        return f.read()
