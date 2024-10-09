import streamlit as st
from pyvis.network import Network
import streamlit.components.v1 as components


# Function to visualize the JIRAs and PRs with the analyzed JIRAs highlighted
def visualize_jira_pr(data, analyzed_jiras):
    # Create pyvis network graph
    net = Network(height='600px', width='100%', directed=False)  # Directed is False for no arrows

    # Add JIRA nodes and PR nodes
    for item in data:
        # Determine color based on whether the JIRA is in analyzed_jiras
        jira_color = "lightgreen" if item["jira"] in analyzed_jiras else "lightgrey"

        # Add JIRA nodes as rectangles with default color or light green if analyzed
        net.add_node(item["jira"],
                     label=f'{item["jira"]}\n({item["probability"]:.2f})',  # Probability on a new line
                     shape="box",  # Box shape for rectangles
                     color=jira_color)

        # Add PR nodes and edges between JIRA and PRs
        for pr in item["prs"]:
            # Set PR node color based on whether the parent JIRA is analyzed
            pr_color = "lightgreen" if item["jira"] in analyzed_jiras else "lightgrey"
            net.add_node(pr, label=pr, shape="ellipse", color=pr_color)
            # Set the edge to be just a line with no arrowhead, also reduce length for PR connections
            net.add_edge(item["jira"], pr, color="black", length=10, dashes=True, arrows="none")  # No arrows

    # Create edges between JIRA nodes based on relevance score (jira4 -> jira1 -> jira2 -> jira3)
    jira_pairs = [(data[i]['jira'], data[i + 1]['jira']) for i in range(len(data) - 1)]
    for source, target in jira_pairs:
        # Adding black lines (without arrows) between JIRA nodes
        net.add_edge(source, target, color="black", width=2, arrows="none")  # No arrows between JIRA nodes

    # Save and display the graph in Streamlit
    net.save_graph('jira_pr_graph.html')

    # Display the graph in Streamlit using an iframe
    st.title("Knowledge Assistant: JIRA and PR Visualization with Rectangles")
    HtmlFile = open('jira_pr_graph.html', 'r', encoding='utf-8')
    components.html(HtmlFile.read(), height=600)


# Sample data in JSON format
data = [
    {"jira": "jira4", "probability": 0.95, "prs": ["PR7"]},
    {"jira": "jira3", "probability": 0.70, "prs": ["PR5"]},
    {"jira": "jira1", "probability": 0.90, "prs": ["PR1", "PR2"]},
    {"jira": "jira2", "probability": 0.85, "prs": ["PR3", "PR4"]}
]

# Analyzed JIRAs
analyzed_jiras = ["jira4", "jira2"]

# Call the visualization function
visualize_jira_pr(data, analyzed_jiras)
