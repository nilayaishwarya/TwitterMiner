import re
import json

with open('Iphone.json', 'r', newline='\r\n') as f:
    geo_data = {
        "type": "FeatureCollection",
        "features": []
    }
    for line in f:
        #try:
            tweet = json.loads(line)
            if tweet['coordinates']:
                geo_json_feature = {
                    "type": "Feature",
                    "geometry": tweet['coordinates'],
                    "properties": {
                        "text": tweet['text'],
                        "created_at": tweet['created_at']
                    }
                }
                geo_data['features'].append(geo_json_feature)
        #except:
         #   continue
 
# Save geo data
with open('geo_data.json', 'w') as fout:
    fout.write(json.dumps(geo_data, indent=4))