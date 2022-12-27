# FlashCard
A tool to make and use flashcards on the localhost.

* ```pip install fastapi``` if you don'y have it installed aldready
* Then, ```uvicorn main:app --reload```

# The JSON file is where every deck of cards is stored.
* The json file should appear like this:```
* [
    [
        "Title",
        "1"
    ],
    [
        "Quest Test",
        "Ans Test"
    ],
    [
        "Quest Test2",
        "Ans Test2"
    ]
  ]```

* The JSON consists of nested lists.
* Every nested list has a length of 2, 0th index being the question and 1st being the answer.
* The only exception is the nested list at the 0th index, where the title and the current page num of the web app is contained.
