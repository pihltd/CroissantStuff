# Not sure what this is doing, mostly just trying to get my head around how schema.org works
# https://github.com/digitalbazaar/pyld
from pyld import jsonld
import json
import requests
from crdclib import crdclib

cds_graphql_url = "https://dataservice.datacommons.cancer.gov/v1/graphql/"

#DataCatalog context
# https://bioschemas.org/tutorials/howto/howto_add_markup
context = {
    "@context": "https://schema.org",
    "@type": "Dataset",
    "@id": "https://dataservice.datacommons.cancer.gov/#/study/phs002431",
    "http://purl.org/dc/terms/conformsTo": {
        "@type": "CreativeWork",
        "@id": "https://bioschemas.org/profiles/Dataset/1.0-RELEASE"
    }
}

def runBentoAPIQuery(url, query, variables=None):
    # Run a graphQL query on any of the Bento sites.
    headers = {'accept': 'application/json'}
    try:
        if variables is None:
            results = requests.post(url, headers=headers, json={'query': query})
        else:
            results = requests.post(url, headers=headers, json={'query': query, 'variables': variables})
    except requests.exceptions.HTTPError as e:
        return (f"HTTPError:\n{e}")
        
    if results.status_code == 200:
        results = json.loads(results.content.decode())
        return results
    else:
        return (f"Error Code: {results.status_code}\n{results.content}")
    

studyquery = """
query getStudyInfo($phs: String!){
    study(phs_accession: $phs){
      study_description
      phs_accession
      study_acronym
      study_external_url
      index_date
      
  }
}"""

variable = {"phs":"phs002431"}

queryjson = runBentoAPIQuery(cds_graphql_url, studyquery, variable)

for entry in queryjson['data']['study']:
    desc = entry['study_description']
    phs = entry['phs_accession']
    acro = entry['study_acronym']
    exturl = entry['study_external_url']
    timestamp = entry['index_Date']
    
    
#print(queryjson)