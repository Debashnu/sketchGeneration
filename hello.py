import streamlit as st
from model import GenerativeModel  # Ensure this module is available and correctly implemented
import re
import networkx as nx
import matplotlib.pyplot as plt

class Component:
    def __init__(self, name, type, pins):
        self.name = name
        self.type = type
        self.pins = pins

class Connection:
    def __init__(self, from_component, from_pin, to_component, to_pin):
        self.from_component = from_component
        self.from_pin = from_pin
        self.to_component = to_component
        self.to_pin = to_pin

def analyze_code(code):
    components = {}
    connections = []
    for line in code.splitlines():
        if line.startswith("component"):
            match = re.match(r"component (\w+) (\w+)(\((\d+(,\d+)*)\))?", line)
            if match:
                name, type, _, pins = match.groups()
                pins = [int(x) for x in pins.split(",")] if pins else []
                components[name] = Component(name, type, pins)
        elif line.startswith("connect"):
            match = re.match(r"connect (\w+) (\d+) to (\w+) (\d+)", line)
            if match:
                from_component, from_pin, to_component, to_pin = match.groups()
                from_pin = int(from_pin)
                to_pin = int(to_pin)
                connections.append(Connection(from_component, from_pin, to_component, to_pin))
    
    wiring_guide = {}
    for connection in connections:
        from_component = components[connection.from_component]
        to_component = components[connection.to_component]
        from_pin_name = get_pin_name(from_component, connection.from_pin)
        to_pin_name = get_pin_name(to_component, connection.to_pin)
        wiring_guide.setdefault(from_component.name, {})[from_pin_name] = (to_component.name, to_pin_name)
        wiring_guide.setdefault(to_component.name, {})[to_pin_name] = (from_component.name, from_pin_name)
    
    return wiring_guide

def get_pin_name(component, pin_number):
    if component.type == "HC05":
        pin_names = ["VCC", "GND", "TXD", "RXD", "STATE"]
    elif component.type == "Arduino":
        pin_names = [f"Digital {i}" for i in range(14)] + [f"Analog {i}" for i in range(6)]
    else:
        pin_names = [f"Pin {i}" for i in range(component.pins)]
    return pin_names[pin_number]

def generate_circuit_diagram(wiring_guide):
    G = nx.DiGraph()
    for component, pins in wiring_guide.items():
        for pin, connection in pins.items():
            G.add_edge(component + ":" + pin, connection[0] + ":" + connection[1])
    
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 7))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, edge_color='black', linewidths=1, font_size=10)
    plt.axis('off')
    st.pyplot(plt)

# Initialize the GenerativeModel
model = GenerativeModel('gemini-pro')

st.title("Welcome to Arduino Code Generator")

# Input fields for project details and components using columns
col1, col2 = st.columns(2)

with col1:
    project_details = st.text_area('Project Details', 'Please enter your project details or requirements')

with col2:
    components = st.text_area('Components', 'Enter the components you are using')

# Button to generate code
generate_code_button = st.button("Generate Code")
if generate_code_button:
    if len(project_details.strip()) == 0:
        st.warning('Please enter your project details or requirements')
    else:
        try:
            # Generate Arduino code using model.py
            generate_code = model.generate_arduino_code(project_details, components)
            
            # Display generated code
            st.success("Generated Arduino code:")
            st.code(generate_code, language='cpp')
            
            # Offer download button for the generated .ino file
            st.download_button(
                label="Download .ino file",
                data=generate_code,
                file_name="generate_code.ino",
                mime="text/plain"
            )
            
            st.title("Circuit Diagram")
            
            # Button to generate diagram
            if st.button("Generate Diagram"):
                try:
                    wiring_guide = analyze_code(generate_code)
                    generate_circuit_diagram(wiring_guide)
                except Exception as e:  
                    st.error(f"Error generating diagram: {str(e)}")
        except Exception as e:
            st.error(f"Error generating code: {str(e)}")
