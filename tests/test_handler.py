import json
from function.handler import handler

def test_list_tasks(mocker):
    mocker.patch("function.handler.get_all_tasks",
                 return_value=[
                        {
                            "task_id":"123",
                            "title":"Test task",
                            "description":"Test description",
                            "status":"pending"
                            }
                     ]
                 )
    event = {
                "httpMethod":"GET",
                "path":"/tasks"
            }

    result = handler(event, None)
    assert result["statusCode"] == 200

    body = json.loads(result["body"])

    assert len(body["tasks"]) == 1
    assert body["tasks"][0]["task_id"] == "123"


def test_create_task(mocker):
    mocker.patch("function.handler.create_task")

    event = {
                "httpMethod":"POST",
                "path":"/tasks",
                "body": json.dumps(
                        {
                            "title":"Deploy application",
                            "description":"Deploy application to AWS",
                            "status":"pending"
                            }
                    )
            }

    result = handler(event, None)
    assert result["statusCode"] == 201

    body = json.loads(result["body"])

    assert body["title"] == "Deploy application"
    assert body["description"] == "Deploy application to AWS"
    assert body["status"] == "pending"
    assert "task_id" in body


def test_create_task_without_title(mocker):
    mocker.patch("function.handler.create_task")

    event = {
            "httpMethod":"POST",
            "path":"/tasks",
            "body":json.dumps(
                {
                    "description":"Task without title"

                    }

                )

            }
    result = handler(event, None)

    assert result["statusCode"] == 400

    body = json.loads(result["body"])

    assert body["message"] == "title is required"


def test_get_task(mocker):
    mocker.patch("function.handler.get_task",
                 return_value = {
                        "task_id":"123",
                        "title":"Test task",
                        "description":"Test description",
                        "status":"pending"
                     })
    event = {
                "httpMethod":"GET",
                "path":"/tasks/123"
            }

    result = handler(event, None)
    assert result["statusCode"] == 200

    body = json.loads(result["body"])
    assert body["task_id"] == "123"


def test_get_nonexistent_task(mocker):
    mocker.patch("function.handler.get_task",
                 return_value=None
                 )

    event = {
            "httpMethod":"GET",
            "path":"/tasks/999"
            }

    result = handler(event,None)
    assert result["statusCode"] == 404


def test_update_task(mocker):
    mocker.patch("function.handler.get_task",
                 return_value = {
                     "task_id":"123",
                     "title":"Old title",
                     "description":"Old description",
                     "status":"pending"
                     }
                 )

    mocker.patch("function.handler.update_task",
                 return_value = {
                     "task_id":"123",
                     "title":"Updated task",
                     "description":"Updated description",
                     "status":"completed"
                     }
            )

    event = {
                "httpMethod":"PUT",
                "path":"/tasks/123",
                "body": json.dumps(
                    {
                        "title":"Updated task",
                        "description":"Updated description",
                        "status":"completed"
                        }
                    )
            }

    result = handler(event, None)
    assert result["statusCode"] == 200

    body = json.loads(result["body"])

    assert body["title"] == "Updated task"
    assert body["status"] == "completed"


def test_update_nonexistent_task(mocker):
    mocker.patch("function.handler.get_task",
                 return_value=None
                 )

    event = {
            "httpMethod":"PUT",
            "path":"/tasks/999",
            "body":json.dumps(
                {
                    "title":"Updated task"
                    }
                )
            }
    result = handler(event, None)
    assert result["statusCode"] == 404


def test_delete_task(mocker):
    mocker.patch("function.handler.delete_task",
                 return_value={
                     "task_id":"123",
                     "title":"Test task",
                     "description":"Test description",
                     "status":"pending"
                     }
                 )
    event = {
                "httpMethod":"DELETE",
                "path":"/tasks/123"
            }

    result = handler(event, None)
    assert result["statusCode"] == 200

    body = json.loads(result["body"])

    assert body["message"] == "Task deleted"
    assert body["task"]["task_id"] == "123"


def test_delete_nonexistent_task(mocker):
    mocker.patch("function.handler.delete_task",
                 return_value=None
                 )

    event = {
            "httpMethod":"DELETE",
            "path":"/tasks/999"
            }

    result = handler(event, None)
    assert result["statusCode"] == 404


def test_unknown_route():
    event = {
                "httpMethod":"GET",
                "path":"/unknown"
            }

    result = handler(event, None)
    assert result["statusCode"] == 404



def test_http_api_v2_list_tasks(mocker):
    mocker.patch(
        "function.handler.get_all_tasks",
        return_value=[]
    )

    event = {
        "version": "2.0",
        "routeKey": "GET /tasks",
        "rawPath": "/tasks",
        "requestContext": {
            "http": {
                "method": "GET",
                "path": "/tasks"
            }
        }
    }

    result = handler(event, None)

    assert result["statusCode"] == 200
