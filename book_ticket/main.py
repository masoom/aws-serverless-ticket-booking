import json
import os
from boto3 import resource
from boto3.dynamodb.conditions import Key, Attr
import uuid

dynamodb = resource("dynamodb")

tickets_table = dynamodb.Table(os.environ.get("TICKETS_TABLE"))
booked_tickets_table = dynamodb.Table(os.environ.get("BOOKED_TICKETS_TABLE"))

def lambda_handler(event, context):
  print("Lambda has been called!")

  ticket_id = event["ticketID"]
  seats = event["seatsNumber"]
  user_id = event["userID"]

  response = book_ticket(user_id, ticket_id, seats)

  return {
    'body': json.dumps(response)
  }

def book_ticket(user_id, ticket_id, seats):
  # Try to book ticket
  try:
    # Exit the function and raise an error if seat is taken
    if is_seat_taken(ticket_id, seats):
      raise SeatAlreadyTaken
    make_seats_unavailable(ticket_id, seats)
    # If anything goes wrong on the proccess, the seat will be automatically available again
    try:
      book_id = str(uuid.uuid4())
      item = {'bookID': book_id, 'userID': user_id, 'ticketID': ticket_id, 'seats': seats}
      put_response = booked_tickets_table.put_item(Item=item)
      return {"Succcess": True, "Message": "Booking Succcessfull" }
    except Exception:
      make_seats_avaiable(seats)
  except SeatAlreadyTaken:
    return {"Succcess": False, "Message": "The seat you select has already been taken"}

def is_seat_taken(ticket_id, seats):
  ticket = tickets_table.get_item(
    Key={
      'ticketID': ticket_id
    }
  )

  available_seats = ticket["Item"]["availableSeats"]
  is_taken = True

  for seat in seats:
    is_taken *= seat not in available_seats

  return is_taken

def make_seats_unavailable(ticket_id, seats):
  ticket = tickets_table.get_item(
    Key={
      'ticketID': ticket_id
    }
  )

  available_seats = ticket["Item"]["availableSeats"]

  for seat in seats:
    available_seats.remove(seat)

  tickets_table.update_item(
    Key={
      'ticketID': ticket_id
    },
    UpdateExpression='SET availableSeats = :available_seats',
    ExpressionAttributeValues={
      ':available_seats': available_seats if len(available_seats) > 0 else ["null"]
    }
  )

  if len(available_seats) == 0:
    tickets_table.update_item(
      Key={
        'ticketID': ticket_id
      },
      UpdateExpression='SET ticketStatus = :ticket_status',
      ExpressionAttributeValues={
        ':ticket_status': "Unavailable"
      }
    )

def make_seats_avaiable(ticket_id, seats):
  ticket = tickets_table.get_item(
    Key={
      'ticketID': ticket_id
    }
  )

  available_seats = ticket["Item"]["availableSeats"]

  for seat in seats:
    if seat not in available_seats:
      available_seats.add(seat)
      tickets_table.update_item(
        Key={
          'ticketID': ticket_id
        },
        UpdateExpression='SET availableSeats = :available_seats',
        ExpressionAttributeValues={
          ':available_seats': available_seats
        }
      )

class SeatAlreadyTaken(Exception):
  pass
