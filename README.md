# aws-serverless-ticket-booking


![Amazon Go](amazongo.png)

Prorotype of a Ticket Booking app for a fictional Event Booking Website Amazon Go

## Implementation

![Booking Infrastructure Architecture](Event-ticket.jpg)


Lambda Functions


```book_ticket(user_id, ticket_id, seats)```


Response: 
```{
            "body": "{\"Succcess\": true, \"Message\": \"Booking Succcessfull\"}"
          }
```


DynamoDB Structure
###### TICKETS_TABLE

```dynamodb
    ticketID : String
    ticketDate: String
    availableSeats: StringSet
    ticketStatus: String
}
```

###### BOOKED_TICKETS_TABLE

```dynamodb
    ticketID : String
    bookID: String
    seats: StringSet
    userID: String
}
```


Created using API Gateway
/tickets (GET)
/booking (POST)


##### To-DO

###### Messaging 
######  Loyalty
