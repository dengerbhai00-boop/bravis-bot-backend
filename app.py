import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# CORS allow karega ki InfinityFree se data is server par aa sake
CORS(app)

# Uploaded files ko safe rakhne ke liye folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return jsonify({"status": "live", "message": "Bravis Digital Automation Server is running!"})

# YAHAN THIK KIYA HAI: list_methods ko badal kar sirf methods kiya hai
@app.route('/apply-pan', methods=['POST'])
def apply_pan():
    try:
        # 1. Frontend se text data nikalna
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        dob = request.form.get('dob')
        
        print(f"--- New Application Received ---")
        print(f"Name: {name}, Phone: {phone}, DOB: {dob}")
        
        # 2. Frontend se files (documents) nikalna aur save karna
        files = request.files
        for file_key in files:
            file = files[file_key]
            if file.filename != '':
                # Har file ko uploads folder mein save karna
                file.save(os.path.join(UPLOAD_FOLDER, f"{phone}_{file_key}_{file.filename}"))
        
        return jsonify({
            "status": "success",
            "message": f"Data received safely for {name}. Bot automation starting soon."
        }), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Server start karne ke liye
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
