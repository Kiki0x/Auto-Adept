from flask import Flask, render_template, request, jsonify
import pymysql
import google.generativeai as genai
import re
import random
import os  # NEW: Lets Python read your image folders!

app = Flask(__name__)

# --- 1. AI Configuration ---
genai.configure(api_key="ADD YOUR API HERE(I HAVE REMOVED MINE FOR PRIVACY REASONS)")
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 2. Database Configuration ---
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'root123'  # Your MySQL password
DB_NAME = 'car_mentor_db'

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

def clean_price(price_str):
    if not price_str or not isinstance(price_str, str): return 0
    cleaned = re.sub(r'[^\d]', '', price_str)
    return int(cleaned) if cleaned else 0

# --- 3. App Routes ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_ai():
    user_message = request.json.get("message")
    visible_cars = request.json.get("cars_on_screen", "No cars currently visible.")
    other_cars = request.json.get("other_options", "No other options visible.")
    
    system_prompt = f"""
    You are an AI Car Recommendation Mentor for 'AutoAdept'. 
    The user is currently looking at these TOP 3 recommended cars on their screen: {visible_cars}
    The user also has these "More Options" listed further down the screen: {other_cars}
    
    Help the user navigate their car buying journey focusing on financial advisory, technical specs, and lifestyle compatibility.
    If the user asks about the top cars, give specific details.
    If the user asks for other options, recommend cars from the "More Options" list.
    Keep responses helpful, brief (2-3 short sentences max), and pressure-free.
    
    User's request: {user_message}
    """
    
    response = model.generate_content(system_prompt)
    return jsonify({"reply": response.text})

@app.route('/search', methods=['POST'])
def search_cars():
    data = request.json
    
    search_query = data.get('search_query', '').strip()[:50] 
    body_type = data.get('body_type', '')[:20]
    fuel_type = data.get('fuel_type', '')[:20]
    
    try:
        budget = int(data.get('budget', 50000000))
        if budget <= 0: budget = 50000000
    except ValueError:
        budget = 50000000
        
    try:
        seats = int(data.get('seats', 0))
        if seats < 0 or seats > 15: seats = 0
    except ValueError:
        seats = 0

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM cars WHERE 1=1"
            params = []

            if search_query:
                sql += " AND (Make LIKE %s OR Model LIKE %s)"
                params.extend(['%' + search_query + '%', '%' + search_query + '%'])
            if body_type and body_type != 'All Types':
                sql += " AND Body_Type LIKE %s"
                params.append('%' + body_type + '%')
            if fuel_type and fuel_type != 'All Types':
                sql += " AND Fuel_Type LIKE %s"
                params.append('%' + fuel_type + '%')
            
            if seats == 8:
                sql += " AND Seating_Capacity >= %s"
                params.append(seats)
            elif seats > 0:
                sql += " AND Seating_Capacity = %s"
                params.append(seats)

            cursor.execute(sql, tuple(params))
            all_matching_cars = cursor.fetchall()
            
            valid_cars = []
            print_debug_count = 0  # NEW: Tracks our radar prints!
            
            for car in all_matching_cars:
                raw_price = car.get('Ex-Showroom_Price') or car.get('Ex_Showroom_Price') or car.get('ex-showroom_price') or '0'
                car['Ex-Showroom_Price'] = raw_price 
                
                price = clean_price(str(raw_price))
                if price > 0 and price <= budget:
                    car['Clean_Price'] = price
                    
                    # 1. Generate the exact filename (NOW BULLETPROOF)
                    raw_make = str(car.get('Make') or car.get('make') or car.get('MAKE') or '')
                    raw_model = str(car.get('Model') or car.get('model') or car.get('MODEL') or '')
                    raw_variant = str(car.get('Variant') or car.get('variant') or car.get('VARIANT') or '')
                    
                    clean_make = re.sub(r'[^a-z0-9]', '', raw_make.lower())
                    clean_model = re.sub(r'[^a-z0-9]', '', raw_model.lower())
                    clean_variant = re.sub(r'[^a-z0-9]', '', raw_variant.lower())
                    
                    filename = f"{clean_make}_{clean_model}_{clean_variant}.jpg"
                    
                    # 2. BULLETPROOF PATH: Locks onto the exact folder app.py is in!
                    base_dir = os.path.dirname(os.path.abspath(__file__))
                    image_path = os.path.join(base_dir, 'static', 'images', filename)
                    
                    # 3. Tag it
                    car['has_image'] = os.path.exists(image_path) 
                    
                    # 4. PRINT TO TERMINAL
                    if print_debug_count < 5:
                        print(f"\n🔎 RADAR CHECK: Looking for -> {image_path}")
                        print(f"   Result: {'✅ FOUND' if car['has_image'] else '❌ NOT FOUND'}")
                        print_debug_count += 1
                        
                    # Also print a giant celebration message if it EVER finds one!
                    if car['has_image'] and print_debug_count >= 5:
                         print(f"🎉 SUCCESS: Found image for {filename}!")
                    
                    valid_cars.append(car)
            
            # The Sorting Logic
            if search_query == '' and budget == 50000000 and fuel_type in ['', 'All Types'] and body_type in ['', 'All Types'] and seats == 0:
                random.shuffle(valid_cars)
                valid_cars.sort(key=lambda x: not x.get('has_image', False))
            else:
                valid_cars.sort(key=lambda x: x['Clean_Price'])
                
        return jsonify({"results": valid_cars})
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
