import yaml
yaml_version_format = {'version': [{'version.placeholder': {'file_id.placeholder': 'id.placeholder'}}],
                       'version_history': [{'v.placeholder': {'file_id.placeholder': 'id.placeholder'}}]}
yaml_string_format = str(yaml.dump(yaml_version_format))

with open('versions_.yaml', 'w') as f:
    f.write(yaml_string_format)