import streamlit as st
import re
import matplotlib.pyplot as plt
import networkx as nx

# Sample function to simulate generating code
def generate_code():
    return """
led = Actuator(LED_PIN)
temp_sensor = Sensor(A1)
servo_motor = Actuator(9)
"""

# Function to parse the code and extract components and connections
def parse_code(code):
    components = {}
    for line in code.splitlines():
        match = re.match(r"(\w+)\s*=\s*(\w+)\((.*)\)", line)
        if match:
            var_name, component, args = match.groups()
            components[var_name] = {'type': component, 'args': [arg.strip() for arg in args.split(',')]}
    return components

# Function to generate wiring connections
def generate_connections(components):
    connections = {}
    for var_name, info in components.items():
        if info['type'] == 'Sensor':
            connections[var_name] = {
                'VCC': '5V',
                'GND': 'GND',
                'DATA': info['args'][0]
            }
        elif info['type'] == 'Actuator':
            connections[var_name] = {
                'VCC': '5V',
                'GND': 'GND',
                'CONTROL': info['args'][0]
            }
    return connections

# Function to draw the connection diagram
def draw_diagram(connections):
    G = nx.Graph()
    for component, pins in connections.items():
        for pin, conn in pins.items():
            G.add_edge(component, conn, label=pin)
    
    pos = nx.spring_layout(G)
    plt.figure()
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue')
    labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    st.pyplot(plt)

# Streamlit app
st.title('IoT Project Code Analyzer')

# Generate the code using generate_code()
generated_code = generate_code()

# Display the generated code
st.subheader("Generated Code")
st.code(generated_code, language='python')

# Button to analyze the code and generate diagram
if st.button("Generate Diagram"):
    # Analyze the generated code
    components = parse_code(generated_code)
    st.subheader("Detected Components")
    st.write(components)

    # Generate wiring connections
    connections = generate_connections(components)
    st.subheader("Generated Connections")
    st.write(connections)

    # Draw the connection diagram
    st.subheader("Connection Diagram")
    draw_diagram(connections)
