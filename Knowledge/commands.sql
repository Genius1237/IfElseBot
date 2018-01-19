CREATE TABLE chat_history IF NOT EXISTS 
( qid integer PRIMARY KEY,question text NOT NULL, response text);


CREATE TABLE unkown IF NOT EXISTS 
( qid integer PRIMARY KEY AUTOINCREMENT, question text NOT NULL, reponse text);