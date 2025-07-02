import psycopg2

db_name = 'bank_db'
db_user = 'postgres'
db_password = 'root'
db_host = 'localhost'
db_port = '5432'

# We can also create a function to get the connection and import the function in the Flask app

conn = psycopg2.connect(     

        dbname = db_name,
        user = db_user,
        password = db_password,
        host = db_host,
        port = db_port

)


# create_query = """

#     create table if not exists account_details(
#         account_id int unique not null,
#         account_holder varchar(100) not null,
#         account_balance float not null
#     )

# """

print(conn)

cursor = conn.cursor()

# cursor.execute(create_query)

conn.commit()
