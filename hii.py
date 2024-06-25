import drawsvg as draw
import streamlit as st

# Define IoT Components
iot_components = {
    'microcontroller': 'Arduino Uno',
    'sensors': ['DHT22', 'BMP180'],
    'modules': ['ESP8266 WiFi Module'],
    'actuators': ['Relay Module'],
    'power_supply': '9V Battery'
}

# Mock function to simulate wiring instructions retrieval
def get_wiring_instructions(components):
    return {
        'Arduino Uno': {
            'pins': {
                'DHT22': ['D2', 'GND', '5V'],
                'BMP180': ['A4', 'A5', 'GND', '3.3V'],
                'ESP8266 WiFi Module': ['D10', 'D11', 'GND', '3.3V'],
                'Relay Module': ['D7', 'GND', '5V'],
                '9V Battery': ['GND', 'Vin']
            }
        }
    }

wiring_instructions = get_wiring_instructions(iot_components)

# Generate Wiring Diagram
def create_wiring_diagram(instructions):
    d = draw.Drawing(800, 600, origin='center', displayInline=False)
    
    components = {
        'Arduino Uno': (-200, 0),
        'DHT22': (-100, 100),
        'BMP180': (-100, -100),
        'ESP8266 WiFi Module': (100, 100),
        'Relay Module': (100, -100),
        '9V Battery': (0, 200)
    }

    for component, (x, y) in components.items():
        d.append(draw.Circle(x, y, 20, fill='white', stroke='black'))
        d.append(draw.Text(component, 10, x, y + 30, center=True))
    
    arduino_pins = instructions['Arduino Uno']['pins']

    connections = [
        (components['Arduino Uno'], components['DHT22'], arduino_pins['DHT22']),
        (components['Arduino Uno'], components['BMP180'], arduino_pins['BMP180']),
        (components['Arduino Uno'], components['ESP8266 WiFi Module'], arduino_pins['ESP8266 WiFi Module']),
        (components['Arduino Uno'], components['Relay Module'], arduino_pins['Relay Module']),
        (components['Arduino Uno'], components['9V Battery'], arduino_pins['9V Battery'])
    ]

    for (start, end, pins) in connections:
        start_x, start_y = start
        end_x, end_y = end
        for pin in pins:
            d.append(draw.Line(start_x, start_y, end_x, end_y, stroke='black'))

    d.saveSvg('/mnt/data/iot_wiring_diagram.svg')
    return '/mnt/data/iot_wiring_diagram.svg'

if wiring_instructions:
    svg_file_path = create_wiring_diagram(wiring_instructions)
else:
    st.error("Failed to get wiring instructions.")
    svg_file_path = None

# Streamlit App
st.title("IoT Wiring Diagram Generator")

st.markdown("## Generated Wiring Diagram")
st.write("Here is the wiring diagram based on the provided IoT components:")

if svg_file_path:
    st.image(svg_file_path)
else:
    st.error("No wiring diagram available.")
