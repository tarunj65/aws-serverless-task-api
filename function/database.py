import os
import boto3

TABLE_NAME = os.environ.get("TASKS_TABLE", "tasks-local")

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

def create_task(task):
    table.put_item(Item=task)
    return task

def get_all_tasks():
    response = table.scan()
    return response.get("Items", [])

def get_task(task_id):
    response = table.get_item(Key={"task_id": task_id})
    return response.get("Item")

def update_task(task_id, title, description, status):
    response = table.update_item(Key = {"task_id": task_id},
                                 UpdateExpression = (
                                     "SET title = :title, "
                                     "description = :description, "
                                     "#status = :status"
                                     ),
                                 ExpressionAttributeNames={
                                        '#status':"status"
                                     },
                                 ExpressionAttributeValues={
                                     ":title": title,
                                     ":description": description,
                                     ":status": status
                                     },
                                 ReturnValues="ALL_NEW"
                                 )
    return response.get("Attributes")

def delete_task(task_id):
    response = table.delete_item(
            Key={"task_id": task_id},
            ReturnValues="ALL_OLD")

    return response.get("Attributes")
