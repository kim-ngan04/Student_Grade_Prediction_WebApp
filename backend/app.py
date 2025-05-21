from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import os

app = Flask(__name__)
CORS(app)

# Load model
model = joblib.load('models/decision_tree_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Nhận dữ liệu JSON từ request
        input_data = request.get_json()
        print("Received data:", input_data)  # Debug line
        
        # Chuyển đổi input_data từ dictionary sang dataframe
        df = pd.DataFrame([input_data])
        print("Created DataFrame:", df)  # Debug line
        
        # One-hot encoding
        df_encoded = pd.get_dummies(df)
        print("After encoding:", df_encoded.columns)  # Debug line
        
        # Đảm bảo có đủ cột giống như lúc training
        missing_cols = set(model.feature_names_in_) - set(df_encoded.columns)
        for col in missing_cols:
            df_encoded[col] = 0
        
        # Sắp xếp cột theo thứ tự của model
        df_encoded = df_encoded[model.feature_names_in_]
        print("Final columns:", df_encoded.columns)  # Debug line
        
        # Dự đoán bằng model
        prediction = float(model.predict(df_encoded)[0])
        print("Prediction:", prediction)  # Debug line
        
        # Xếp loại điểm
        if prediction >= 18:
            status = "Xuất sắc"
        elif prediction >= 16:
            status = "Giỏi"
        elif prediction >= 13:
            status = "Khá" 
        elif prediction >= 10:
            status = "Trung bình"
        else:
            status = "Yếu"
            
        return jsonify({
            'success': True,
            'prediction': prediction,
            'status': status,
            'message': f'Điểm dự đoán: {prediction:.1f}/20 - {status}'
        })
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Debug line
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)