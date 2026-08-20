from function.handler import handler

def test_list_tasks():
    event = {
                "httpMethod":"GET",
                "path":"/tasks"
            }

    result = handler(event, None)
    assert result["statusCode"] == 200

def test_create_task():
    event = {
                "httpMethod":"POST",
                "path":"/tasks"
            }

    result = handler(event, None)
    assert result["statusCode"] == 201

def test_get_task():
    event = {
                "httpMethod":"GET",
                "path":"/tasks/123"
            }

    result = handler(event, None)
    assert result["statusCode"] == 200

def test_update_task():
    event = {
                "httpMethod":"PUT",
                "path":"/tasks/123"
            }

    result = handler(event, None)
    assert result["statusCode"] == 200

def test_delete_task():
    event = {
                "httpMethod":"DELETE",
                "path":"/tasks/123"
            }

    result = handler(event, None)
    assert result["statusCode"] == 200

def test_unknown_route():
    event = {
                "httpMethod":"GET",
                "path":"/unknown"
            }

    result = handler(event, None)
    assert result["statusCode"] == 404
