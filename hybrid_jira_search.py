# ----------------------------
# Step 2: Hybrid Semantic + Fuzzy JIRA ID Search
# ----------------------------

async def hybrid_jira_search(kernel_memory, collection_name, user_query, known_prefixes, top_k=5):
    results = []

    # Step 1: Semantic Search
    semantic_results = await kernel_memory.search(
        collection_name,
        user_query,
        limit=top_k,
        min_relevance_score=0.5
    )

    # Step 2: Try fuzzy match on JIRA ID from user query
    fuzzy_jira_id = find_fuzzy_jira_id(user_query, known_prefixes)

    # Step 3: Boost relevance score if entry contains the matched JIRA ID
    for r in semantic_results:
        boost = 0.0
        if fuzzy_jira_id and fuzzy_jira_id in r.text:
            boost += 0.5  # big boost for ID match
        results.append((r.relevance + boost, r))

    # Step 4: Sort by boosted score and return top_k
    results.sort(key=lambda x: x[0], reverse=True)
    top_results = [r[1] for r in results[:top_k]]

    return top_results
