from flask import Flask, render_template, request, Response
import requests
import json
import os

app = Flask(__name__)

api_base_url="https://your-api-gateway-stage-url"
user_id = "sample-user-name"

@app.route("/tickets")
def get_tickets():
  req_url = api_base_url + "/tickets"
  response = requests.get(req_url)

  response_text = json.loads(response.text)
  tickets = json.loads(response_text["body"])

  return render_template("tickets.html", tickets=tickets)

@app.route("/book_ticket", methods=["GET", "POST"])
def book_ticket():

  ticket_id = request.args.get('ticket_id')
  if request.method == "GET":
    available_seats = get_available_seats(ticket_id)

    return render_template("book_ticket.html", seats=available_seats)
  elif request.method == "POST":
    seats=list(request.form.to_dict().keys())
    response = make_book(ticket_id, user_id, seats)
    if response["Succcess"]:
      return Response(json.dumps(response), status=200)
    else:
      return Response(json.dumps(response), status=400)

def get_available_seats(ticket_id):
  req_url = api_base_url + "/tickets"
  response = requests.get(req_url)
  response_text = json.loads(response.text)
  tickets = json.loads(response_text["body"])

  for ticket in tickets:
    if ticket["ticketID"] == ticket_id:
      return ticket["availableSeats"]

  return []

def make_book(ticket_id, user_id, seats):
  req_url = api_base_url + "/booking"
  payload = {"ticketID": ticket_id, "userID": user_id, "seatsNumber": seats}
  req = requests.post(req_url, json=payload)
  response = json.loads(req.text)["body"]
  return json.loads(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
