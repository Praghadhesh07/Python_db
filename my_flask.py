from flask import Flask, request, jsonify

from database import conn,cursor #, create_query

# conn = get_connection()
# cursor = conn.cursor()


app = Flask(__name__)

details=[]

@app.route('/',methods=['GET'])

def check_flask():
    return "flask is running successfully", 200


# @app.route('/create_table',methods=['POST'])

# def create_table():

#     print(conn)

#     cursor = conn.cursor()

#     cursor.execute(create_query)

#     conn.commit()
#     return 'Table created successfully.', 201


@app.route('/create_account',methods=['POST'])

def create_account():

    client = request.get_json()
    
    insert_query = f""" 

        insert into account_details (account_id, account_holder, account_balance) values ({client['account_id']}, '{client['account_holder']}', {client['account_balance']})
"""
    cursor = conn.cursor()
    cursor.execute(insert_query)
    conn.commit()
    return 'account created.', 201


@app.route('/get_accounts',methods=['GET'])

def get_accounts():

    fetch_query = """
    select * from account_details order by account_id asc
"""
    cursor.execute(fetch_query)

    rows = cursor.fetchall()

    # To get column names
    columns = [col[0] for col in cursor.description]

    # Convert row to dictionary
    result = [dict(zip(columns, row)) for row in rows]

    return jsonify(result), 200



@app.route('/get_specific_account/<int:account_id>', methods=['GET'])
def get_specific_account(account_id):
    fetch_one_query = "SELECT * FROM account_details WHERE account_id = %s"
    cursor.execute(fetch_one_query, (account_id,))
    row = cursor.fetchone()

    # To get column names
    columns = [col[0] for col in cursor.description]

    # Convert row to dictionary
    result = dict(zip(columns, row))
    return jsonify(result), 200



# @app.route('/update_specific_detail/<int:account_id>', methods=['PATCH'])
# def update_specific_detail(account_id):
#     client = request.get_json()
#     patch_query = "UPDATE account_details SET account_balance = %s WHERE account_id = %s"
#     cursor.execute(patch_query, (client['account_balance'], account_id))
#     conn.commit()
#     return 'Account balance updated successfully.', 200

@app.route('/update_specific_detail/<int:account_id>', methods=['PATCH'])
def update_specific_detail(account_id):
    client = request.get_json()
    patch_query = f"UPDATE account_details SET account_balance = {client['account_balance']} WHERE account_id = {account_id}"
    cursor.execute(patch_query)
    conn.commit()
    return 'Account balance updated successfully.', 200


@app.route('/update_account_details/<int:account_id>', methods=['PUT'])
def update_details(account_id):
    client = request.get_json()
    fields = []
    values = []

    if 'account_id' in client:
        fields.append('account_id = %s')
        values.append(client['account_id'])
    if 'account_holder' in client:
        fields.append('account_holder = %s')
        values.append(client['account_holder'])
    if 'account_balance' in client:
        fields.append('account_balance = %s')
        values.append(client['account_balance'])

    put_query = f"UPDATE account_details SET {', '.join(fields)} WHERE account_id = %s"
    values.append(account_id)

    cursor.execute(put_query, values)
    conn.commit()
    return 'Account details updated successfully', 200
    # return jsonify({'error': 'Account not found'}), 404


@app.route('/delete_account/<int:account_id>',methods=['DELETE'])

def delete_account(account_id):
   
    delete_query = f"""
        delete from account_details where account_id = {account_id}
"""
    cursor.execute(delete_query)
    conn.commit()
    return 'Account deleted successfully.', 200


app.run(port=8000)