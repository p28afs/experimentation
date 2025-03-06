import hashlib
from langchain.graphs import LLMGraphTransformer, Neo4jGraph

# Function to compute a unique hash from text content.
def generate_doc_hash(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

# Initialize the transformer with your custom prompt and additional instructions.
transformer = LLMGraphTransformer(
    llm=llm,
    custom_prompt=custom_prompt,
    additional_instructions=additional_instructions
)

# Assume you have a function to split your document into chunks.
document_text = "Your full document content here..."
document_chunks = split_document_into_chunks(document_text)  # Replace with your splitter function.

# Transform the chunks into graph documents.
graph_documents = transformer.transform_to_graph_documents(document_chunks)

# Add deduplication metadata (such as doc_hash) to each graph document.
for doc in graph_documents:
    # Generate a hash from the document's full text.
    doc_hash = generate_doc_hash(doc.full_text)
    if not hasattr(doc, "metadata") or doc.metadata is None:
        doc.metadata = {}
    doc.metadata["doc_hash"] = doc_hash
    doc.metadata["source_doc"] = "Your_Document_Name"  # Adjust as needed

# Connect to your Neo4j graph database.
graph = Neo4jGraph(
    url="bolt://localhost:7687",
    database="neo4j",
    username="neo4j",
    password="your_password"
)

# When adding documents to the graph, use a MERGE strategy based on the unique identifier.
graph.add_graph_documents(graph_documents, baseEntityLabel=True, include_source=True)
