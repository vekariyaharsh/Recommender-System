from flask import Flask, request, jsonify
from neo4j import GraphDatabase

app = Flask(__name__)

# Connect to Neo4j
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "12345678"))

@app.route('/recommend', methods=['GET','POST'])
def recommend():
    actor_name = request.args.get("actor", "")
    genre = request.args.get("genre", "")

    cypher_query = """
    MATCH (d:Person {name: $director})-[:ACTED_IN]->(:Movie)-[:IN_GENRE]->(g:Genre)
WITH d, collect(DISTINCT g) AS directorGenres
UNWIND directorGenres AS genre
MATCH (rec:Movie)-[:IN_GENRE]->(genre)
WHERE NOT (d)-[:ACTED_IN]->(rec)
WITH DISTINCT rec
RETURN rec.title AS title, rec.imdb_rating AS rating , rec.DIRECTED
ORDER BY rating DESC
LIMIT 10 """

    with driver.session() as session:
        results = session.run(cypher_query, director=actor_name, genre=genre)
        output = [dict(record) for record in results]
        return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)
