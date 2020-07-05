import json
import os
from boto3 import resource

dynamodb = resource("dynamodb")

tickets_table = dynamodb.Table(os.environ.get("TICKETS_TABLE"))

# Dumps json and converts SETS to LIST
class SetEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, set):
      return list(obj)
    return json.JSONEncoder.default(self, obj)

def lambda_handler(event, context):
    tickets = tickets_table.scan()["Items"]
    print(tickets)

    return {
      'body': json.dumps(tickets, cls=SetEncoder)
    }
