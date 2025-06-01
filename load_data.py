
from neo4j import GraphDatabase
import csv

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "12345678")

driver = GraphDatabase.driver(URI, auth=AUTH)

def load_movies(csv_path):
    with driver.session() as session, open(csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            session.write_transaction(add_movie, row)

def add_movie(tx, row):
    tx.run("""
        MERGE (m:Movie {title: $title})
        SET m.imdb_rating = toFloat($imdb_rating),
            m.year = toInteger($year),
            m.certification = $certification,
            m.metascore = toInteger($metascore),
            m.duration = toInteger($duration)

        WITH m
        FOREACH (dir IN split($director, ",") |
          MERGE (d:Person {name: trim(dir)})
          MERGE (d)-[:DIRECTED]->(m))

        FOREACH (actor IN split($actors, ",") |
          MERGE (a:Person {name: trim(actor)})
          MERGE (a)-[:ACTED_IN]->(m))

        FOREACH (g IN split($genre, ",") |
          MERGE (genre:Genre {name: trim(g)})
          MERGE (m)-[:IN_GENRE]->(genre))
    """, {
        "title": row["Title"],
        "imdb_rating": row["IMDb Rating"],
        "year": row["Year"],
        "certification": row["Certificates"],
        "metascore": row["MetaScore"] or 0,
        "duration": row["Duration (minutes)"] or 0,
        "director": row["Director"],
        "actors": row["Star Cast"],
        "genre": row["Genre"]
    })

if __name__ == "__main__":
    load_movies("D:/Other Ideas/movie_Rec/IMDb_Dataset.csv")
    print("✅ Data loaded into Neo4j.")
