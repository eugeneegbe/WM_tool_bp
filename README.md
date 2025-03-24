# Wikimedia Flask-React Blueprint
Making it simple for Wikimedia developers to develop tools to facilitate editing on Wikimedia projects such as #Wikidata, #Wikipedia etc. Built from [React flask app](https://github.com/Devking/React-Flask-App)

## Running the application 
To compile the src js to usable js:

```
npm run build
```

This will use Webpack and Babel to turn the code you wrote into something that can be understood.

To run the Flask server:

```
flask run
```

*Note: If yyour tool uses a database, you should add models, create a datase, edit the env file before running the following command from the project root directory*

```
python -m tool.maintenace.setup_db .
```
This should add the required tables to the database.
