def translate_schema(raw_data):
    data = raw_data['data']
    try:
        id = data['id']
    except Exception as e:
        id = data['data']['id']
    return {
        'id': id,
    }
