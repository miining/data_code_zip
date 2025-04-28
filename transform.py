#transform Drug and DISEASE json add CSV
import json
import pandas as pd


concept_df = pd.read_csv('concept.csv', sep='\t', usecols=['concept_code', 'vocabulary_id', 'concept_id'])
concept_mapping = {
    str(row['concept_code']): (row['vocabulary_id'], int(row['concept_id']))
    for _, row in concept_df.iterrows()
}


with open('records.json', 'r', encoding='utf-8-sig') as f:
    records = json.load(f)

# 3. 변환
new_data = []
node_id_mapping = {}
node_counter = 1
rel_counter = 1

def map_node(node):
    global node_counter
    old_id = node['identity']
    labels = node['labels']
    props = node['properties']

    if 'DISEASE' in labels:
        source_code = props.get('class_id')
        source_name = props.get('name')
        voca_id, concept_id = concept_mapping.get(str(source_code), ('MeSH', None))
    elif 'Drug' in labels:
        source_code = props.get('source_id')
        source_name = props.get('name')
        voca_id, concept_id = concept_mapping.get(str(source_code), ('RxNorm', None))
    else:
        return None

    if old_id not in node_id_mapping:
        node_id_mapping[old_id] = node_counter
        node_counter += 1

    new_node = {
        "identity": node_id_mapping[old_id],
        "labels": labels,
        "properties": {
            "source_code": source_code,
            "source_name": source_name,
            "voca_id": voca_id,
            "concept_id": concept_id
        },
        "elementId": node['elementId']
    }
    return new_node

for record in records:
    n = record['n']
    m = record['m']
    r = record['r']

    n_mapped = map_node(n)
    m_mapped = map_node(m)

    if n_mapped and m_mapped:
        rel_mapped = {
            "identity": rel_counter,
            "start": node_id_mapping[r['start']],
            "end": node_id_mapping[r['end']],
            "type": r['type'],
            "properties": r['properties'],
            "elementId": r['elementId'],
            "startNodeElementId": r['startNodeElementId'],
            "endNodeElementId": r['endNodeElementId']
        }
        rel_counter += 1

        new_data.append({
            "n": n_mapped,
            "r": rel_mapped,
            "m": m_mapped
        })


with open('transformed_records.json', 'w') as f:
    json.dump(new_data, f, indent=2)

print(f"{len(new_data)}개 저장됨 -> 'transformed_records.json'")
