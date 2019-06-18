# Instructions for setup

* Before starting, make sure you have Python 3.6 and Postgres 9.6 installed in your machine.

* Clone the repository and run the following command from root directory of the cloned project.

  $ source setup.sh
  
  If you get an error installing postgres connector library, add the following to PATH and run the command again:
  
  _"/Applications/Postgres.app/Contents/Versions/9.6/bin"_   **// Specify your Postgres version**

* The development server should be running by now. You are ready to make api calls.

* First run the following api to populate some data in db:
    - http://localhost:8000/populate_db/ **[GET]**

* Add some prices:
  -   http://localhost:8000/prices/ **[POST]**

  Post Data:
  ```
  {
    "date_from": "2019-03-29", 
    "date_to": "2019-04-10", 
    "origin_code": "NOFRK" , 
    "destination_code": "CNNBO", 
    "price": 200,
    "currency": "INR" // optional
   }
   ```

    You may add an additional field "currency" to specify the currency of the price.
    Please get a list of supported currencies from the url: http://localhost:8000/currencies/ **[GET]**

* Now, call the GET apis:
  
  - http://127.0.0.1/rates?date_from=2019-03-30&date_to=2019-04-02&origin=NOFRK&destination=norway_south_east **[GET]**
  
  - http://127.0.0.1/rates_null?date_from=2019-03-30&date_to=2019-04-02&origin=NOFRK&destination=norway_south_east **[GET]**

**P.S: To view the saved data, visit: http://localhost:8000/admin/ Username=admin, password=admin**
