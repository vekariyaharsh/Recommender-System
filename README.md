# 🎬 IMDb Movie Recommendation System using Neo4j, Flask, and Streamlit

This is a full-stack movie recommendation system that transforms a structured IMDb dataset into a graph database using **Neo4j**, serves movie recommendations via a **Flask API**, and presents a user interface with **Streamlit**.

---

---

## 📊 Dataset Format

The `IMDb_Dataset.csv` includes:

| Column         | Description                                  |
|----------------|----------------------------------------------|
| `Title`        | Movie title                                  |
| `IMDb Rating`  | IMDb rating (float)                          |
| `Year`         | Year of release                              |
| `Certificates` | MPAA certificate (e.g. PG-13, R)             |
| `Genre`        | Comma-separated genres (e.g. Action, Drama)  |
| `Director`     | Comma-separated directors                    |
| `Star Cast`    | Comma-separated leading actors               |
| `MetaScore`    | Metacritic score (integer)                   |
| `Duration`     | Runtime in minutes                           |

---

## 🧠 Graph Model in Neo4j

| Node Label | Properties                           |
|------------|--------------------------------------|
| `Movie`    | `title`, `year`, `imdb_rating`, `duration` |
| `Person`   | `name` (used for both actors and directors) |
| `Genre`    | `name`                               |

### 🔗 Relationships

| Relationship            | Meaning                        |
|-------------------------|--------------------------------|
| `(:Person)-[:ACTED_IN]->(:Movie)`  | Person acted in movie |
| `(:Person)-[:DIRECTED]->(:Movie)`  | Person directed movie |
| `(:Movie)-[:IN_GENRE]->(:Genre)`   | Movie belongs to genre |

---

## 🛠️ Installation Guide

### 1. Clone the Repository

git clone https://github.com/YOUR_USERNAME/imdb-neo4j-recommender.git
cd imdb-neo4j-recommender
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt


Configure Neo4j
Install Neo4j Desktop

Create a new database named MoviesDB

Update auth=("neo4j", "your-password") in import_movies.py and backend/app.py

cd frontend
streamlit run app.py
cd backend
python app.py

http://localhost:5000/recommend?actor=Tom Hanks&genre=Drama
