import OperationService

def test_create():
    var = {
        "id": 0,
        "type": 1,
        "sum": 0,
        "datetime": "2024-05-19T21:15:08.212Z",
        "userId": 0
    }
    assert OperationService.create('test')