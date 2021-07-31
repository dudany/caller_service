# caller id extractor Service

# project overview
This service receives requests with phone number and will return their related caller name.
The server runs with Flask framework. when running the server the data is preprocessed then loaded once.


# Data overview
### the data schema is:
1. name : -> string
2. phone_number : -> string (contains "-")
3. source: -> string
4. num_of_records: -> int
5. location: -> string 
6. work_email: -> string (all blanks)

### fields description and assumptions

1. location : -> it's a country, it can be full or short i.g sweden or SE
2. name : -> caller name may contain emojis.
3. phone number : -> string ,format is "123-123-1234" phone numbers. this field isn't unique - so several rows can appear on the same number.
4. number of records : -> int, number of times this caller appeared with this info, bigger number represents more repetitions. 
5. source : -> string, source represents from what source we got this caller, I decided to
   weight those source by the order: ['vendor', 'email_signature', 'address_book', 'community', 'scarping'], so we could 
   determine which source is more reliable.

### data cleaning procedure
1. name: all emojis will be removed, also name prefixes such as Mr. and trailing spaces.
2. location: found data set that maps 2-digit country code to full name
3. work_email: is empty for some reason, so I remove the column
4. phone number: expected to be in format of "123-123-1234"

### interesting phone number with cases:
1. 385-391-2014 name duplication with **"teresa b"** and **"teresa ben"**
2. 745-493-1979 name with emoji that is removed
3. bad input phone number "123-123-123a"
3. missing phone number "123-123-1234"

### please follow these installing instructions:
1. create virtual env under .env in project with python 3.6 interpreter
2. install the required python module
```bash
pip install -r my_service/requiremnts.txt
```
3. run server by running python my_service/service_run.py 
4. send requests

### exceptions
1. on bad phone number input I will raise bad input exception **BadPhoneNumberInput**.
2. if name is not appearing for the input will be raised **NameNotFoundError**
3. if the source of the user were bad raise **BadSourceException**

### HTTP REQUEST
```bash
curl -d '{"phone_number": "440-804-3781"}' -X POST http://127.0.0.1:8080/caller_id -H "Content-Type: application/json"
```

### SERVER
server is running on one process with multi threaded default option that is built in flask.
the requests to the service would be sync.

## To postpone
* make an option get requests with source parameter.
* calibrate better the sorting.
* change the service to work with a-sync threads.  
* create and connect the service to a real DB, would pick from 2 options :
  1. SQL based db, as the schema is always the same.
  2. Elastic Search to search on strings. 
