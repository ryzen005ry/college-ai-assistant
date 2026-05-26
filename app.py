from flask import Flask, render_template, request, jsonify
from ml_models import CollegeMLSystem
import database

app = Flask(__name__)
ml_system = CollegeMLSystem()
database.init_db()

@app.route('/')
def home(): return render_template('base.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    results = None
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        marks = int(request.form.get('marks'))
        if form_type == 'course':
            results = {'type': 'course', 'data': ml_system.predict_course(request.form.get('group'), marks)}
        elif form_type == 'admission':
            results = {'type': 'admission', 'data': ml_system.predict_admission(marks)}
    return render_template('predict.html', results=results)

@app.route('/chatbot')
def chatbot(): return render_template('chatbot.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    user_msg = request.json.get('message', '').lower()
    response = "I'm sorry, I didn't understand. Try asking about 'fees', 'hostel', 'courses', or 'placements'."
    if 'fee' in user_msg: response = "Our B.Tech fee is $5000/year. BSc is $3000/year."
    elif 'hostel' in user_msg: response = "We have 4 boys and 3 girls hostels with WiFi."
    elif 'course' in user_msg: response = "We offer B.Tech, MBBS, BSc, and BCom."
    elif 'placement' in user_msg: response = "95% placement rate! Top recruiters: Google, Microsoft."
    return jsonify({"reply": response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
