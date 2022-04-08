db = db.getSiblingDB("quotes");
db.quotes.drop();

db.quotes.insertMany([
    {
        "_id": ObjectId("62484e1cae6196db6f6929eb"),
        "author": "J.R.R. Tolkien",
        "text": "There's some good in this world, Mr. Frodo, and it's worth fighting for."
    },
    {
        "_id": ObjectId("62486227a3090907a460b5af"),
        "author": "Rene Descartes",
        "text": "I think therefore I am."
    },
    {
        "_id":  ObjectId("6248f4b2ae6196db6f6929ec"),
        "author": "Mahatma Ghandi",
        "text": "You must be the change you wish to see in the world."
    }
    
]);

