import sys
import gpxpy
import gpxpy.gpx
from xml.etree import ElementTree as ET

def combine_gpx(files):
    combined_gpx = gpxpy.gpx.GPX()

    # Define a list of colors for routes
    route_colors = ['Red', 'Blue', 'Green', 'Orange', 'Purple', 'Yellow']

    for i, file in enumerate(files):
        with open(file, 'r') as gpx_file:
            gpx_data = gpxpy.parse(gpx_file)
            
            # Assign a color to each route
            route_color = route_colors[i % len(route_colors)]

            for track in gpx_data.tracks:
                combined_gpx.tracks.append(track)

                # Assign color to the track
                for segment in track.segments:
                    for point in segment.points:
                        point.extensions = {
                            'color': route_color
                        }

    return combined_gpx

def generate_output(gpx_data):
    # Convert GPX data to XML and add color information
    xml_data = gpx_data.to_xml()
    root = ET.fromstring(xml_data)
    
    for trk in root.findall('.//trk'):
        color = trk.find('.//color').text
        for trkseg in trk.findall('.//trkseg'):
            for trkpt in trkseg.findall('.//trkpt'):
                ET.SubElement(trkpt, 'extensions')
                ET.SubElement(trkpt.find('.//extensions'), 'color').text = color

    # Return the modified XML as a string
    return ET.tostring(root).decode('utf-8')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python combine_gpx.py file1.gpx file2.gpx ...")
        sys.exit(1)

    file_list = sys.argv[1:]
    combined_gpx_data = combine_gpx(file_list)
    combined_output = generate_output(combined_gpx_data)

    # Print the combined GPX data to stdout
    print(combined_output)

