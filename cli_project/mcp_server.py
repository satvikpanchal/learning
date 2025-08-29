from mcp.server.fastmcp import FastMCP
from pydantic import Field
from mcp.server.fastmcp.promts import base

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# A tool to read a doc
@mcp.tool(
    name="read_doc",
    description="Read a document from the document store.",
)
def read_document(
    doc_id: str = Field(description="Id of the document to read")
    ):

    if doc_id not in docs:
        raise ValueError(f"Document {doc_id} not found")

    return docs[doc_id]


# A tool to edit a doc
@mcp.tool(
    name="edit_doc",
    description="Edit a document in the document store by replacing a string in the document with a new string.",
)
def edit_document(
    doc_id: str = Field(description="Id of the document to edit"),
    old_string: str = Field(description="The string to replace, must match the string in the document exactly, including capitalization and spacing."),
    new_string: str = Field(description="The new string to replace the old string with"),
):
    if doc_id not in docs:
        raise ValueError(f"Document {doc_id} not found")

    docs[doc_id] = docs[doc_id].replace(old_string, new_string)

# A resource to return all doc id's
@mcp.resource(
    "docs://dcouments",
    mime_type="application/json",
)
def list_docs():
    return list(docs.keys())

# A resource to return the contents of a particular doc
@mcp.resource(
    f"docs://documents/{doc_id}",
    mime_type="text/plain"
)
def fetch_doc(doc_id: str):
    if doc_id not in docs:
        raise ValueError(f"Document {doc_id} not found")
    return docs[doc_id]

@mcp.tool(
    name="format",
    description="Rewrite a document in markdown format.",
)
def format_document(
    doc_id: str = Field(description="Id of the document to format")):
    prompt = f"""
    Rewrite the following document in markdown format:

    <instructions>
    - Rewrite the document in markdown format.
    - Keep the document's structure and content.
    - Use the document's title as the markdown file name.
    </instructions>

    <document>
    {docs[doc_id]}
    </document>
    """
    return [base.UserMessage(prompt)]


# A tool to summarize a doc
@mcp.tool(
    name="summarize_doc",
    description="Summarize a document in the document store.",
)
def summarize_document(doc_id: str = Field(description="Id of the document to summarize")):
    if doc_id not in docs:
        raise ValueError(f"Document {doc_id} not found")

    return docs[doc_id]


if __name__ == "__main__":
    mcp.run(transport="stdio")
