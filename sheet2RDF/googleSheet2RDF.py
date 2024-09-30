import gspread
from oauth2client.service_account import ServiceAccountCredentials
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, SKOS

# Set up Google Sheets API
def get_google_sheet(sheet_url, sheet_name):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.worksheet(sheet_name)
    
    return worksheet.get_all_records()

# Define the RDF namespaces
DATA_METHODS = Namespace("https://raw.githubusercontent.com/ritamargherita/DataMethods/main/DataMethods.ttl#")
W3ID = Namespace("https://w3id.org/")
SKOS_NS = Namespace(SKOS)

# Convert the spreadsheet rows to RDF triples
def convert_to_rdf(sheet_data, output_file):
    g = Graph()
    
    # Bind namespaces to prefixes
    g.bind('skos', SKOS)
    g.bind('data', DATA_METHODS)
    g.bind('w3id', W3ID)
    
    for row in sheet_data:
        # Generate a stable URI using w3id and the row data
        subject = URIRef(W3ID[row['ID']])
        
        # Add basic RDF triples
        g.add((subject, RDF.type, DATA_METHODS['Concept']))
        
        # Assuming the spreadsheet has columns 'Label', 'Description', and 'BroaderTerm'
        g.add((subject, SKOS_NS.prefLabel, Literal(row['Label'], lang="en")))
        g.add((subject, SKOS_NS.definition, Literal(row['Description'], lang="en")))
        
        # Handle broader term (hierarchical relation)
        if row.get('BroaderTerm'):
            broader_term = URIRef(W3ID[row['BroaderTerm']])
            g.add((subject, SKOS_NS.broader, broader_term))
    
    # Serialize the graph to Turtle format
    g.serialize(destination=output_file, format='turtle')

# Main function
if __name__ == "__main__":
    # Replace with your Google Spreadsheet URL and worksheet name
    sheet_url = 'https://docs.google.com/spreadsheets/d/YOUR_SPREADSHEET_ID'
    sheet_name = 'Sheet1'
    
    # Get the Google Spreadsheet data
    sheet_data = get_google_sheet(sheet_url, sheet_name)
    
    # Convert the data to RDF and save it to a Turtle file
    output_file = 'output.rdf'
    convert_to_rdf(sheet_data, output_file)
    print(f"RDF has been written to {output_file}")
