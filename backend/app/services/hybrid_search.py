from rank_bm25 import BM25Okapi

from app.db.chroma import collection
from app.services.embedding_service import get_embedding


def reciprocal_rank_fusion(rank, k=60):
    return 1 / (k + rank)


def hybrid_search(
    question: str,
    user_id: str,
    pdf_id: str | None = None,
    n_results: int = 5
):

    data = collection.get(
        where={"user_id": user_id},
        include=["documents", "metadatas"]
    )

    documents = data["documents"]
    metadatas = data["metadatas"]

    if not documents:
        return []

    if pdf_id:

        filtered_docs = []
        filtered_meta = []

        for doc, meta in zip(
            documents,
            metadatas
        ):

            if meta["pdf_id"] == pdf_id:

                filtered_docs.append(doc)
                filtered_meta.append(meta)

        documents = filtered_docs
        metadatas = filtered_meta

    if not documents:
        return []

    tokenized_docs = [
        doc.split()
        for doc in documents
    ]

    bm25 = BM25Okapi(
        tokenized_docs
    )

    bm25_scores = bm25.get_scores(
        question.split()
    )

    bm25_ranked = sorted(
        zip(
            documents,
            metadatas,
            bm25_scores
        ),
        key=lambda x: x[2],
        reverse=True
    )[:10]

    query_embedding = get_embedding(
        question
    )

    vector_results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=10
    )

    scores = {}

    # BM25 scores
    for rank, (doc, meta, _) in enumerate(
        bm25_ranked,
        start=1
    ):

        scores[doc] = {
            "score": reciprocal_rank_fusion(rank),
            "meta": meta
        }

    # Vector scores
    for rank, (doc, meta) in enumerate(
        zip(
            vector_results["documents"][0],
            vector_results["metadatas"][0]
        ),
        start=1
    ):

        if doc not in scores:

            scores[doc] = {
                "score": 0,
                "meta": meta
            }

        scores[doc]["score"] += reciprocal_rank_fusion(
            rank
        )

    final_results = sorted(
        scores.items(),
        key=lambda x: x[1]["score"],
        reverse=True
    )

    return [
        {
            "doc": doc,
            "meta": data["meta"]
        }
        for doc, data in final_results[:n_results]
    ]
