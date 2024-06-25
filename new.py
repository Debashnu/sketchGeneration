import streamlit as st
import re

# Predefined component types and their typical connections
component_wiring = {
    'Sensor': {'VCC': '5V', 'GND': 'GND', 'DATA': 'pin'},
    'Actuator': {'VCC': '5V', 'GND': 'GND', 'CONTROL': 'pin'},
    # Add more component types and their connection rules here
}

# Function to analyze Arduino .ino code and generate connections
def analyze_code(code, components):
    connections = []
    for line in code.splitlines():
        match = re.match(r"(\w+)\s*=\s*(" + "|".join(re.escape(comp) for comp in components) + r")\((.*)\);", line)
        if match:
            var_name, component, args = match.groups()
            component_type = 'Unknown'
            if 'Sensor' in component:
                component_type = 'Sensor'
            elif 'Actuator' in component:
                component_type = 'Actuator'
            # Add more rules if needed
            
            if component_type in component_wiring:
                connection = f"{var_name} ({component}) connections:"
                for pin in component_wiring[component_type]:
                    conn = component_wiring[component_type][pin]
                    if conn == 'pin':
                        conn = args.split(',')[0].strip()
                    connection += f"\n - {pin} to {conn}"
                connections.append(connection)
    return connections

# Streamlit app
def main():
    st.title('Arduino Connection Generator')

    # Text area for pasting Arduino .ino code
    st.subheader('Paste Arduino .ino Code')
    code = st.text_area("Input Arduino Code", height=400)

    # Text area for entering component names
    st.subheader('Enter Component Names')
    components_input = st.text_area("Input Components (comma-separated)", height=100, placeholder="Sensor1, Actuator1, Sensor2")

    if st.button("Generate Connections"):
        if code.strip() == "" or components_input.strip() == "":
            st.warning('Please input both Arduino .ino code and component names')
        else:
            try:
                # Split the components input into a list
                components = [comp.strip() for comp in components_input.split(',')]
                st.subheader("Detected Components")
                st.write(components)

                # Analyze the code to generate connections
                connections = analyze_code(code, components)
                st.subheader("Generated Connections")
                for connection in connections:
                    st.write(connection)
            except Exception as e:
                st.error(f"Error processing code: {e}")

if __name__ == "__main__":
    main()
