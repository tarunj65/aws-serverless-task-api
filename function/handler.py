import json
import uuid

def response(status_code, body):
    return {
           "statusCode": status_code,
            "headers": {
                    "Content-Type": "application/json"
                },
            "body": json.dumps(body)
            }


def handler(event, context):
    """
    AWS Lambda entry point.
    Handles API Gateway requests for the task API.
    """

    method = event.get("httpMethod", "")
    path = event.get("path", "")

    if method == "GET" and path == "/tasks":
        return response(
                200, {
                        "message": "Task API is working",
                        "action": "list_tasks"
                    }
                )

    if method == "POST" and path == "/tasks":
        task_id = str(uuid.uuid4())

        return response(
                201, {
                        "message": "Task created",
                        "task_id": task_id
                    }
                )

    if method == "GET" and path.startswith("/tasks/"):
        task_id = path.split("/")[-1]

        return response(
                200, {
                        "message": "Task retrieved",
                        "task_id": task_id
                    }
                )

    if method == "PUT" and path.startswith("/tasks/"):
        task_id = path.split("/")[-1]

        return response(
                    200, {
                            "message": "Task updated",
                            "task_id": task_id
                        }
                )

    if method == "DELETE" and path.startswith("/tasks/"):
        task_id = path.split("/")[-1]

        return response(
                    200, {
                            "message": "Task deleted",
                            "task_id": task_id
                        }
                )

    return response(
                404,
                     {
                        "message": "Route not found"
                    }
            )
