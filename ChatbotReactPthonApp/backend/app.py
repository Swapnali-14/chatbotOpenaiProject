from flask import Flask, request, jsonify
import mysql.connector
import openai  # For using GPT-3 or any other open-source model
from flask_cors import CORS 
# Initialize Flask app
app = Flask(__name__)

# Set your OpenAI API key and uncomment below line whenever running
# openai.api_key = "Your-api-key"

CORS(app)

# MySQL database connection
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="chatbot_db"
    )
    return conn



# Summarize supplier information (this can be an LLM or a simpler approach)
def summarize_info(info):
    try:
        # Call OpenAI API to generate summary
        response = openai.Completion.create(
           model="gpt-3.5-turbo",  # Use the newer models like gpt-3.5-turbo or gpt-4
           prompt="Translate the following English text to French: 'Hello, how are you?'",
           max_tokens=60
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error summarizing: {str(e)}"

# Query endpoint
@app.route('/query', methods=['POST'])
def query():
    query_data = request.get_json()  # Get the query data from frontend
    query = query_data['query']

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if "brand" in query:
        cursor.execute("SELECT * FROM products WHERE brand LIKE %s", (f"%{query.split('brand ')[1]}%",))
    elif "suppliers" in query:
        cursor.execute("SELECT * FROM suppliers WHERE product_categories_offered LIKE %s", (f"%{query.split('suppliers provide ')[1]}%",))
        print("SELECT * FROM suppliers WHERE product_categories_offered LIKE %s", (f"%{query.split('suppliers ')[1]}%",))
    elif "product" in query:
          cursor.execute("SELECT * FROM products WHERE name LIKE %s", (f"%{query.split('product ')[1]}%",))

    else:
        return jsonify({"error": "Query not recognized"}), 400
      
    data = cursor.fetchall()
    print(data)
    conn.close()

    if not data:
        return jsonify({"error": "No results found"}), 404

    # Summarize data for the response
    summarized_response = ""
    for item in data:
        summarized_response += summarize_info(str(item)) + "\n"

    return jsonify({"message": summarized_response})

if __name__ == "__main__":
    app.run(debug=True)
