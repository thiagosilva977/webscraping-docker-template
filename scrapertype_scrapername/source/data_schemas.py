import pyarrow as pa


def get_schema(source_name: str):
    if source_name == 'test_site':
        selected_schema = pa.schema([
            ('id', pa.string()),
            ('title', pa.string()),
            ('description', pa.string()),
            ('reviews', pa.int32()),
            ('stars', pa.int32()),
            ('price', pa.float32()),
            ('url', pa.string()),
            ('image_url', pa.string()),
            ('collected_date', pa.string()),
            ('source', pa.string()),
        ])
    else:
        selected_schema = None

    return selected_schema
