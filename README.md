# Tic Tac Toe server!

## Description

A server for playing tic tac toe, made using sockets and JSON

## Running project

To run this project, you need:

    - pyenv with python 3.8 installed

    - pipenv

and install the dependencies:

    $ make setup
  
After that you can:

* start the server:

      $ make run

* start testing client:

      $ make run_client

## Message format

### Server message format

The server responses are in JSON, containing the following fields:

```json
  {
    "status": "status of the player",
    "error_type": "type of the error",
    "message": "error context",
    "board": "array representing the board"
  }
```

* The `error_type` will only appear in case of error, so check if the `status` field is `error` first.

* The `message` field is only used when the status is `error`

* The `board` field is only used when the status is either `opponent` or `play`

* The `defeat` or `victory` will wait for an JSON with the `continue` field, which may contain `y` or `n`

#### status types

| status   |  description                                     |
|----------|--------------------------------------------------|
| error    | An error ocurred. Check the error_type field     |
| waiting  | Name saved. Waiting for another player           |
| matched  | Matched with another player. The game will begin |
| play     | The server is waiting for your move              |
| opponent | Wait your opponent's move                        |
| victory  | You won!                                         |
| defeat   | You lost...                                      |


#### Error types

| error_type     |  description                                                                                                                                       |
|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| OPPONENT_LEFT  | Your opponent has left the game, you will be moved back to the matcher. The client should wait for the message with status "matched" again.        |
| INVALID_FORMAT | The client is not sending the correct format (JSON). See [client message format](#client-message-format). The server will wait for another message |
| INVALID_VALUES | The values are either out of bounds (1 <= value <= 3) or targetting a position already chosen on the board |

### Client message format

The first message should be the player's name, in the following format:

```json
  {
    "my_name":"player name"
  }
```

`WARNING!`: If the message doesn't contain the field `my_name` the connection will be closed by the server without any response.

upon receiving `my_name` message, the server will register it and send to the matcher.

after being matched with another player, the game will start. The game messages should follow the format:

```json
  {
    "line": "integer value between 1 and 3",
    "column": "integer value between 1 and 3"
  }
```

### After winning or losing

The Client will receive an `status` with `defeat` or `victory`. The Client must send a JSON with the `continue` field, which may contain `y` or `n`. 

* `y`: The server will keep the connection and try to start another game

* `n`: The server will stop the connection

#### Example:

```json
  {
    "continue": "y",
  }
```

### An example of the message exchange

| Server   | message direction | Client_1      |
|----------|-------------------|---------------|
| -        | <--               | my_name       |
| waiting  | -->               | -             |
| matched  | -->               | -             |
| play     | -->               | -             |
| -        | <--               | {line, column} |
| opponent | -->               | -             |
| play     | -->               | -             |
| -        | <--               | {line, column} |