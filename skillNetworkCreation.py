import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

# -------------------------------
# Data Parsing and Processing
# -------------------------------
def parse_skill_data(file_path):
    """
    Parse and process skill data from the provided Excel file.
    
    Expected Excel columns: 
      - 'Element ID' : The job type identifier.
      - 'Element Name' : Unique identifier for a skill (e.g., '2.A.1.a').
      - 'Region'  : (Optional) Region information associated with the job.
      
    Returns:
        A pandas DataFrame containing the skill data.
    """
    try:
        df = pd.read_csv(file_path)
        print(df)
        # Validate required columns
        print("Columns in the file:", df.columns)
        required_columns = ['Element ID', 'Element Name']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        return df
    except Exception as e:
        print(f"Error parsing skill data: {e}")
        return None

# -------------------------------
# Graph Construction
# -------------------------------
def create_weighted_skill_graph(df):
    """
    Create a weighted network graph where:
      - Each node represents a unique skill.
      - An edge between two nodes is added if the skills appear in the same job type.
      - The edge weight corresponds to the number of job types where the two skills co-occur.
      
    Also assigns a 'region' attribute to nodes if available.
    
    Returns:
        A NetworkX graph representing the skill network.
    """
    G = nx.Graph()
    co_occurrence = defaultdict(int)
    
    # Group by job type to count co-occurrences
    grouped = df.groupby('Element ID')
    for job_type, group in grouped:
        skills = group['Element Name'].unique()
        for i in range(len(skills)):
            for j in range(i+1, len(skills)):
                pair = tuple(sorted((skills[i], skills[j])))
                co_occurrence[pair] += 1
    
    # Add nodes with optional region attribute if available
    unique_skills = df['Element Name'].unique()
    for skill in unique_skills:
        regions = df[df['Element Name'] == skill]['Region'].unique() if 'Region' in df.columns else None
        G.add_node(skill, region=regions[0] if regions is not None and len(regions) > 0 else None)
    
    # Add weighted edges based on co-occurrence counts
    for (skill1, skill2), weight in co_occurrence.items():
        G.add_edge(skill1, skill2, weight=weight)
    
    return G

# -------------------------------
# Contextual Regional Insights
# -------------------------------
def get_regional_insights(df):
    """
    Generate contextual insights based on regional data.
    
    For example, count the number of unique job types per region.
    
    Returns:
        A dictionary with regional insights.
    """
    insights = {}
    if 'Region' in df.columns:
        # Count unique job types per region
        region_counts = df.groupby('Region')['JobType'].nunique().to_dict()
        insights['job_types_by_region'] = region_counts
    else:
        insights['job_types_by_region'] = "No regional data available."
    return insights

# -------------------------------
# Interactive Visualization
# -------------------------------
def visualize_skill_graph(G):
    """
    Visualize the weighted skill network graph using matplotlib.
    Nodes represent skills; edges are drawn with thickness proportional to their weight.
    """
    pos = nx.spring_layout(G)  # Determine node positions using a force-directed layout
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue')
    
    # Draw edges with widths proportional to co-occurrence weight
    edges = G.edges(data=True)
    weights = [data['weight'] for (_, _, data) in edges]
    nx.draw_networkx_edges(G, pos, width=[w * 0.5 for w in weights], edge_color='gray')
    
    # Draw node labels
    nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')
    
    plt.title("Weighted Skill Network Graph")
    plt.axis('off')
    plt.show()

# -------------------------------
# User Interface (Command-Line)
# -------------------------------
def user_interface(G):
    """
    A simple command-line interface for users to input a Skill ID and retrieve:
      - The top 10 most related skills based on co-occurrence.
      - A placeholder for job types where these skills co-occur.
    """
    skill_id = input("Enter a Skill ID (e.g., 2.A.1.a): ").strip()
    if skill_id not in G.nodes:
        print("Skill ID not found in the network.")
        return
    
    # Retrieve neighboring skills and sort them by edge weight
    neighbors = G[skill_id]
    sorted_neighbors = sorted(neighbors.items(), key=lambda x: x[1]['weight'], reverse=True)
    top_neighbors = sorted_neighbors[:10]
    
    print(f"\nTop related skills for {skill_id}:")
    for neighbor, attr in top_neighbors:
        print(f"- {neighbor} (Co-occurrence weight: {attr['weight']})")
    
    # Placeholder: Display job types for these skill pairs
    print("\nJob types for these skill pairs: [Feature to be implemented]\n")

# -------------------------------
# Recommendation Engine (Stub)
# -------------------------------
def recommend_courses(skill_id, G):
    """
    Recommend skill development courses based on co-occurrence data.
    This is a stub function for demonstration purposes.
    """
    print(f"Recommended courses for skill {skill_id}:")
    # Placeholder recommendations – in a real implementation, these would be data-driven.
    recommendations = ["Course A", "Course B", "Course C"]
    for course in recommendations:
        print(f"- {course}")

# -------------------------------
# Real-Time Data Integration (Stub)
# -------------------------------
def integrate_real_time_data():
    """
    Stub for integrating real-time labor market data.
    In practice, this function would fetch live data from external APIs.
    """
    print("Integrating real-time labor market data... [Feature to be implemented]")

# -------------------------------
# Interactive Regional Map (Stub)
# -------------------------------
def display_interactive_map(df):
    """
    Stub for creating an interactive map that displays the regional skill network and job types.
    Libraries like Plotly or Folium could be used in a full implementation.
    """
    print("Displaying interactive regional map... [Feature to be implemented]")

# -------------------------------
# Reporting Module (Stub)
# -------------------------------
def generate_report(G, insights, output_file):
    """
    Stub for generating a downloadable report detailing skill relationships
    and regional workforce recommendations.
    
    The report could be generated in PDF, CSV, or another format.
    """
    print(f"Generating report and saving to {output_file}... [Feature to be implemented]")
    # Example: Write insights to a text file (for demonstration)
    with open(output_file, "w") as f:
        f.write("Skill Network Report\n")
        f.write("====================\n\n")
        f.write("Regional Insights:\n")
        f.write(str(insights))
        f.write("\n\n[Additional report details to be added here]\n")

# -------------------------------
# Main Function
# -------------------------------
def main():
    # Parse the skill data from the Excel file
    data_file = "/Users/injohtanwani/Documents/CS 502/skills-list.xlsx"
    df = parse_skill_data(data_file)
    if df is None:
        return

    # Create the weighted skill network graph with regional segmentation
    G = create_weighted_skill_graph(df)

    # Get and display contextual regional insights
    insights = get_regional_insights(df)
    print("Regional Insights:", insights)

    # Visualize the skill network graph
    visualize_skill_graph(G)

    # Provide a simple user interface for analyzing skill relationships
    user_interface(G)

    # Run the recommendation engine (stub demonstration)
    recommend_courses("2.A.1.a", G)

    # Integrate real-time labor market data (stub demonstration)
    integrate_real_time_data()

    # Display interactive regional map (stub demonstration)
    display_interactive_map(df)

    # Generate a report (stub demonstration)
    generate_report(G, insights, "output/report.txt")

if __name__ == "__main__":
    main()
