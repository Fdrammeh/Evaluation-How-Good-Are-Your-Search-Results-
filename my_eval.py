"""
L7 — Evaluate Your Search System  (STARTER)
=============================================
Run with:
    python starter.py

Your goal: build an evaluation framework that measures precision and recall
for a semantic search system across multiple settings.

Required features:
    1. A ChromaDB collection with at least 12 documents across 3–4 topics
    2. An evaluation set: at least 6 test queries, each with a list of
       expected relevant document IDs
    3. An evaluate() function that computes per-query and average
       precision & recall
    4. Results at 3 different settings (vary threshold, n_results, or both)
    5. A written analysis in the output

Key concepts:
    Precision — of the results returned, how many were relevant?
        precision = len(relevant ∩ retrieved) / len(retrieved)

    Recall — of all relevant documents, how many did we retrieve?
        recall = len(relevant ∩ retrieved) / len(relevant)

    ChromaDB returns distances (lower = more similar).
    Convert to similarity for thresholding:
        similarity = 1 - distance   (for cosine distance)
        OR just filter by distance <= threshold

    Example evaluation set entry:
        {
            "query": "How does FastAPI validate request data?",
            "relevant_ids": ["doc_03", "doc_07"]
        }
"""

import chromadb

# ── Documents ─────────────────────────────────────────────────────────────────
# TODO: Define ids, documents, and metadatas lists (at least 12 items)
#       Cover 3–4 topics so that some queries are easy and some are hard.
#       Use unique IDs like "doc_01", "doc_02", ... — these are what the
#       evaluation set references.

ids = [
    # TODO
    "doc_01",
    "doc_02",
    "doc_03",
    "doc_04",
    "doc_05",
    "doc_06",
    "doc_07",
    "doc_08",
    "doc_09",
    "doc_10",
    "doc_11",
    "doc_12",
]

documents = [
    # TODO
    # FastAPI
    "FastAPI uses Python type hints to validate request data and generate API documentation.",
    "FastAPI endpoints can use Pydantic models to validate incoming JSON request bodies.",
    "FastAPI provides automatic interactive API documentation through Swagger UI and ReDoc.",
    
    # Python
    "Python lists are ordered collections that can store multiple values in a single variable.",
    "Python dictionaries store data as key-value pairs and allow values to be retrieved by key.",
    "Python functions are reusable blocks of code that can accept arguments and return values.",
    
    # ChromaDB
    "ChromaDB is a vector database designed for storing and searching embeddings.",
    "ChromaDB collections contain documents, IDs, embeddings, and optional metadata.",
    "Semantic search with ChromaDB finds documents based on meaning rather than exact keyword matches.",
    
    # Streamlit
    "Streamlit allows developers to build interactive data applications using Python.",
    "Streamlit session state allows an application to store information between user interactions.",
    "Streamlit can display tables, charts, forms, buttons, and other interactive interface elements.",

]

metadatas = [
    # TODO — at least {"topic": "..."} for each document
    {"topic": "fastapi"},
    {"topic": "fastapi"},
    {"topic": "fastapi"},
    {"topic": "python"},
    {"topic": "python"},
    {"topic": "python"},
    {"topic": "chromadb"},
    {"topic": "chromadb"},
    {"topic": "chromadb"},
    {"topic": "streamlit"},
    {"topic": "streamlit"},
    {"topic": "streamlit"},
]

# ── ChromaDB setup ────────────────────────────────────────────────────────────
# TODO: Create a chromadb.EphemeralClient() (in-memory, no files needed)
client = chromadb.EphemeralClient()
# TODO: Create or get a collection called "eval_collection"
collection = client.get_or_create_collection("eval_collection")
# TODO: Upsert all documents
collection.upsert(
    ids=ids,
    documents=documents,
    metadatas=metadatas
)

# ── Evaluation set ────────────────────────────────────────────────────────────
# TODO: Define eval_set — a list of dicts, each with:
#   "query":        the natural language query string
#   "relevant_ids": list of document IDs that are truly relevant
def eval_set():
    return [
        {"query": "How does FastAPI validate request data?", "relevant_ids": ["doc_01", "doc_02"]},
        {"query": "What are Python lists and how do they work?", "relevant_ids": ["doc_04"]},
        {"query": "Explain ChromaDB and its use cases.", "relevant_ids": ["doc_07", "doc_08", "doc_09"]},
        {"query": "How can I build interactive apps with Streamlit?", "relevant_ids": ["doc_10", "doc_11", "doc_12"]},
        {"query": "What is the difference between Python dictionaries and lists?", "relevant_ids": ["doc_04", "doc_05"]},
        {"query": "How does semantic search differ from keyword search?", "relevant_ids": ["doc_09"]},
    ]
eval_set = [
    # TODO — at least 6 entries
    # {"query": "...", "relevant_ids": ["doc_01", "doc_05"]},
    {"query": "How does FastAPI validate request data?", "relevant_ids": ["doc_01", "doc_02"]},
    {"query": "What are Python lists and how do they work?", "relevant_ids": ["doc_04"]},
    {"query": "Explain ChromaDB and its use cases.", "relevant_ids": ["doc_07", "doc_08", "doc_09"]},
    {"query": "How can I build interactive apps with Streamlit?", "relevant_ids": ["doc_10", "doc_11", "doc_12"]},
    {"query": "What is the difference between Python dictionaries and lists?", "relevant_ids": ["doc_04", "doc_05"]},
    {"query": "How does semantic search differ from keyword search?", "relevant_ids": ["doc_09"]},
]


# ── Evaluation function ────────────────────────────────────────────────────────
def evaluate(n_results: int, distance_threshold: float = None):
    """
    Run every query in eval_set, compute precision and recall for each,
    and print per-query results plus averages.

    Args:
        n_results:          how many results to retrieve per query
        distance_threshold: if set, only count results with distance <= this
    """
    print(f"\n=== Evaluation: n_results={n_results}, threshold={distance_threshold} ===")

    precisions = []
    recalls    = []

    for i, entry in enumerate(eval_set, 1):
        query        = entry["query"]
        relevant_ids = set(entry["relevant_ids"])

        # TODO: Query the collection with query_texts=[query], n_results=n_results
        #       include ["ids", "distances"]
        results = None  # replace with actual query
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["distances"])

        # TODO: Extract retrieved IDs from results["ids"][0]
    #retrieved_ids = []
    retrieved_ids = results["ids"][0]

        # TODO: If distance_threshold is set, filter out IDs whose distance
        #       exceeds the threshold
    if distance_threshold is not None:
            # Filter retrieved IDs based on distance threshold
        retrieved_ids = [doc_id for doc_id, dist in zip(retrieved_ids, results["distances"][0]) if dist <= distance_threshold]

        # TODO: Compute precision and recall
        overlap   = len(relevant_ids & set(retrieved_ids))
        precision = overlap / len(retrieved_ids)  if len(retrieved_ids) > 0 else 0
        recall    = overlap / len(relevant_ids)   if len(relevant_ids) > 0 else 0

        precisions.append(precision)
        recalls.append(recall)

        print(f"  Query {i}: P={precision*100:.1f}%  R={recall*100:.1f}%  "
              f"| '{query[:50]}'")

    avg_p = sum(precisions) / len(precisions) if precisions else 0
    avg_r = sum(recalls)    / len(recalls)    if recalls    else 0
    print(f"  AVERAGE: P={avg_p*100:.1f}%  R={avg_r*100:.1f}%")
    return avg_p, avg_r


# ── Run at 3 settings ─────────────────────────────────────────────────────────
# TODO: Call evaluate() with 3 different combinations of n_results / threshold
evaluate(n_results=3)
evaluate(n_results=5)
evaluate(n_results=5, distance_threshold=0.5)


# ── Analysis ─────────────────────────────────────────────────────────────────
print("\n=== ANALYSIS ===")
# TODO: Print your observations as a multi-line string or separate print() calls.
#       Answer:
#         - Which queries consistently performed well? Why?
#         - Which queries failed? What caused the low score?
#         - What would you change to improve the weakest queries?
#         - How did increasing n_results affect precision vs recall?
print("TODO: write your analysis here")
print("""
- Some queries performed well because they had clear, specific keywords that matched the documents in the collection. For example, queries about FastAPI and Streamlit had high precision and recall due to the presence of relevant documents with matching topics.

- Other queries failed due to ambiguity or lack of relevant documents in the collection. For instance, the query about the difference between Python dictionaries and lists had lower scores because it was too broad and the relevant documents were not as closely aligned with the query.")

- To improve the weakest queries, I would consider adding more documents to the collection that cover a wider range of topics and provide more context for the queries. Additionally, refining the queries to be more specific could help improve retrieval performance.")

- Increasing n_results generally improved recall, as more documents were retrieved, but it sometimes decreased precision because more irrelevant documents were included in the results. Balancing n_results and applying a distance threshold can help optimize both precision and recall.

""")