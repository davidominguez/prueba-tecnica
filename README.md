# Omnios Technical Test - API Creation
### Solution development
The following technologies have been used to develop this project:
- FastAPI: used for API creation.
- Pydantic: used for data validation.
- MongoDB: NoSQL database for the persistence of semi-structured data, as well as to efficiently search documents.

A class hierarchy has been applied for the two data schemas of the application since they have fields in common, thus implementing a base class with these common fields and extending this class to implement the custom fields of each of the models.

Different design patterns have been used for the code such as:
- adapter: use has been made of an interface with abstract methods which are implemented according to the database used. This makes the code maintainable in case the database is changed in the future.

### Possible improvements
- Use of ``singleton`` design pattern for the creation of database connections, as these are usually expensive and keeping the same instance could improve performance.
- Use of custom indexes for the database, in order to make queries more efficient (text indexes...).
- Products should be stored in a database.
### Execution

We should create the ```.env``` file in the root folder of the project (next to the ```docker-compose.yml``` file). This file will have the same structure as the ```.env.sample``` file.

In our case it is enough to rename the file from ````.env.sample```` to ```.env``` since this is a demo and the credentials are for testing.

To run the application just run ````docker compose up -d```.



### URLs of the services
- Swagger: http://localhost:8000/docs