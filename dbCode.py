#I used ChatGPT to help me write some of these, and to help me rearrange them in a more conceptually sound way. 
import pymysql
import creds
import boto3
from boto3.dynamodb.conditions import Key

### ----- MySQL CONNECTION SETUP ----- ###
def get_conn():
    conn = pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db,
        autocommit=True  # ensures changes persist without needing .commit()
    )
    return conn

### ----- MYSQL HELPER FUNCTION ----- ###
def execute_query(query, args=(), fetch=True):
    conn = get_conn()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute(query, args)
            if fetch:
                result = cur.fetchall()
                return result
    except Exception as e:
        print("Database error:", e)
    finally:
        conn.close()

### ----- MYSQL GENERAL FUNCTIONS ----- ###
def get_list_of_dictionaries():
    query = "SELECT Name, Population FROM country LIMIT 10;"
    return execute_query(query)

### ----- USER CRUD FUNCTIONS (MySQL) ----- ###
def get_users():
    query = "SELECT * FROM users"
    return execute_query(query)

def create_user(username, password, first_name=None, last_name=None, travel_history=None, travel_destination=None):
    query = """
        INSERT INTO users (username, password, first_name, last_name, travel_history, travel_destination)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    execute_query(query, (username, password, first_name, last_name, travel_history, travel_destination), fetch=False)

def read_users():
    query = "SELECT * FROM users;"
    return execute_query(query)

def read_user_by_id(user_id):
    query = "SELECT * FROM users WHERE id = %s;"
    return execute_query(query, (user_id,))

def update_user(user_id, first_name, last_name, travel_history, travel_destination):
    query = """
        UPDATE users
        SET first_name = %s,
            last_name = %s,
            travel_history = %s,
            travel_destination = %s
        WHERE id = %s
    """
    execute_query(query, (first_name, last_name, travel_history, travel_destination, user_id), fetch=False)

def update_user_credentials(user_id, new_username, new_password):
    query = "UPDATE users SET username = %s, password = %s WHERE id = %s;"
    execute_query(query, (new_username, new_password, user_id), fetch=False)

def delete_user(user_id):
    query = "DELETE FROM users WHERE id = %s;"
    execute_query(query, (user_id,), fetch=False)

def delete_user_by_name(username):
    query = "DELETE FROM users WHERE username = %s;"
    execute_query(query, (username,), fetch=False)

### ----- MYSQL JOIN EXAMPLE ----- ###
def get_cities_and_languages_by_country(country_name):
    query = """
        SELECT city.Name AS City, countrylanguage.Language
        FROM city
        JOIN country ON city.CountryCode = country.Code
        JOIN countrylanguage ON country.Code = countrylanguage.CountryCode
        WHERE country.Name = %s
        LIMIT 10;
    """
    return execute_query(query, (country_name,))

### ----- DYNAMODB SETUP ----- ###
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('TravelHistory')

### ----- DYNAMODB FUNCTIONS ----- ###
def create_travel_table():
    table = dynamodb.create_table(
        TableName='TravelHistory',
        KeySchema=[
            {'AttributeName': 'username', 'KeyType': 'HASH'},
            {'AttributeName': 'destination', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'username', 'AttributeType': 'S'},
            {'AttributeName': 'destination', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    return table

def add_travel_history(username, destination, date_of_trip):
    response = table.put_item(
        Item={
            'username': username,
            'destination': destination,
            'date_of_trip': date_of_trip
        }
    )
    return response

def get_travel_history(username):
    response = table.query(
        KeyConditionExpression=Key('username').eq(username)
    )
    return response['Items']