from utils.util_functions import process_jsonl_file

def test_process_zst_file(client, mocker):
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.content = b'some compressed data'

    mock_open = mocker.patch('builtins.open', mocker.mock_open())

    mocker.patch('zstandard.ZstdDecompressor.copy_stream')

    mock_process_jsonl_file = mocker.patch('utils.util_functions.process_jsonl_file')

    response = client.post('/process-zst')
    assert response.status_code == 200
    assert response.json == {"status": "completed"}

def test_process_jsonl_file(tmpdir, mocker):
    sample_jsonl = tmpdir.join("sample.jsonl")
    sample_jsonl.write('{"key": "value"}\n')

    mock_send_to_silver = mocker.patch('utils.util_functions.send_to_silver')

    process_jsonl_file(str(sample_jsonl))

    # Check if send_to_silver was called with the expected data
    mock_send_to_silver.assert_called_once_with([{"data": {"key": "value"}}])
