import json
import os
import uuid

from function.database import (create_task, get_all_tasks, get_task, update_task, delete_task)

def response(status_code, body):
    return {
           "statusCode": status_code,
            "headers": {
                    "Content-Type": "application/json"
                },
            "body": json.dumps(body)
            }

def parse_body(event):
    body = event.get("body")

    if not body:
        return {}

    if isinstance(body, str):
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return {}
    return body



def handler(event, context):
    """
    AWS Lambda entry point.
    Handles API Gateway requests for the task API.
    """
    
    method = event.get("httpMethod", "")
    path = event.get("path", "")
    
    if not method:
        request_context = event.get("requestContext", {})
        http = request_context.get("http", {})

        method = http.get("method", "")
        path = http.get("path", "")

    if method == "GET" and path == "/tasks":
        tasks = get_all_tasks()

        return response(
                200, {
                        "tasks": tasks
                    }
                )

    if method == "POST" and path == "/tasks":
        body = parse_body(event)

        title = body.get("title")
        description = body.get("description", "")
        status = body.get("status", "pending")

        if not title:
            return response(
                400, {
                        "message": "title is required"
                    }
                )

        task = {
                "task_id": str(uuid.uuid4()),
                "title": title,
                "description": description,
                "status": status
                }

        create_task(task)

        return response(201, task)

    if method == "GET" and path.startswith("/tasks/"):
        task_id = path.split("/")[-1]
        
        task = get_task(task_id)
        if not task:
            return response(404, {"message":"Task not found"})
        return response(
                200, task
                )

    if method == "PUT" and path.startswith("/tasks/"):
        task_id = path.split("/")[-1]
        
        body = parse_body(event)
        task = get_task(task_id)

        if not task:
            return response(
                        404,{"message": "Task not found"}
                    )

        updated_task = update_task(
                    task_id,
                    body.get("title", task.get("title")),
                    body.get("description", task.get("description", "")),
                    body.get("status", task.get("status","pending"))
                )

        return response(
                    200, updated_task
                )

    if method == "DELETE" and path.startswith("/tasks/"):
        task_id = path.split("/")[-1]

        deleted_task = delete_task(task_id)

        if not deleted_task:
            return response(
                        404, {"message": "Task not found"}
                    )

        return response(
                    200, {
                            "message": "Task deleted",
                            "task": deleted_task
                        }
                )

    return response(
                404,
                     {
                        "message": "Route not found"
                    }
            )
