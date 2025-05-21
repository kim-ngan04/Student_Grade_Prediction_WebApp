"""
Mã nguồn huấn luyện mô hình dự đoán điểm số sinh viên
Phiên bản nâng cao với phân tích dữ liệu kỹ lưỡng và tối ưu hóa mô hình
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score, KFold
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.feature_selection import SelectFromModel
from sklearn.pipeline import Pipeline
import xgboost as xgb
from sklearn.linear_model import LinearRegression, Ridge, Lasso
import joblib
import os
import warnings
import datetime
import json

# Bỏ qua cảnh báo không cần thiết
warnings.filterwarnings('ignore')

# Tạo thư mục lưu trữ kết quả
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
base_dir = f'training_results_{timestamp}'
models_dir = os.path.join(base_dir, 'models')
plots_dir = os.path.join(base_dir, 'plots')
logs_dir = os.path.join(base_dir, 'logs')

for directory in [models_dir, plots_dir, logs_dir]:
    os.makedirs(directory, exist_ok=True)

# Cũng tạo thư mục models ở thư mục gốc cho Flask API
os.makedirs('models', exist_ok=True)

# Thiết lập log
log_file = os.path.join(logs_dir, 'training_log.txt')

def log_message(message):
    """Ghi log ra file và hiển thị trên console"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry + '\n')

# Bắt đầu quá trình huấn luyện
log_message("===== BẮT ĐẦU HUẤN LUYỆN MÔ HÌNH DỰ ĐOÁN ĐIỂM SỐ SINH VIÊN =====")

# Đọc dữ liệu
log_message("Đang đọc tập dữ liệu...")
try:
    data = pd.read_csv(r'C:\Users\Admin\Downloads\AI\DoAnUngDung_2\csv\student_data_train.csv')
    log_message(f"Đọc dữ liệu thành công: {data.shape[0]} dòng và {data.shape[1]} cột")
except Exception as e:
    log_message(f"Lỗi khi đọc dữ liệu: {str(e)}")
    exit(1)

# Lưu bản sao của dữ liệu gốc
original_data = data.copy()

# Phân tích dữ liệu
log_message("\n=== PHÂN TÍCH DỮ LIỆU ===")

# Thông tin cơ bản về dữ liệu
log_message(f"Kích thước dữ liệu: {data.shape}")
log_message(f"Các cột trong dữ liệu: {', '.join(data.columns.tolist())}")

# Kiểm tra giá trị null
null_counts = data.isnull().sum()
if null_counts.sum() > 0:
    log_message(f"Phát hiện giá trị null trong dữ liệu:\n{null_counts[null_counts > 0]}")
    log_message("Đang xử lý giá trị null...")
    # Xử lý giá trị null nếu có
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    categorical_cols = data.select_dtypes(exclude=[np.number]).columns
    
    # Điền các giá trị null với giá trị trung bình cho cột số và mode cho cột phân loại
    for col in numeric_cols:
        if data[col].isnull().sum() > 0:
            data[col].fillna(data[col].mean(), inplace=True)
    
    for col in categorical_cols:
        if data[col].isnull().sum() > 0:
            data[col].fillna(data[col].mode()[0], inplace=True)
    
    log_message("Đã xử lý xong các giá trị null")
else:
    log_message("Không phát hiện giá trị null trong dữ liệu")

# Thống kê mô tả
log_message("\nThống kê mô tả:")
description = data.describe().T
description['missing'] = data.isnull().sum()
description['dtype'] = data.dtypes
log_message(f"\n{description}")

# Phân tích biến mục tiêu G3
log_message("\nPhân tích biến mục tiêu G3:")
log_message(f"Giá trị trung bình: {data['G3'].mean():.2f}")
log_message(f"Độ lệch chuẩn: {data['G3'].std():.2f}")
log_message(f"Giá trị nhỏ nhất: {data['G3'].min()}")
log_message(f"Giá trị lớn nhất: {data['G3'].max()}")
log_message(f"Phân phối tứ phân vị: {data['G3'].quantile([0.25, 0.5, 0.75]).tolist()}")

# Vẽ biểu đồ phân phối của G3
plt.figure(figsize=(10, 6))
sns.histplot(data['G3'], kde=True, bins=20)
plt.title('Phân phối điểm số G3', fontsize=14)
plt.xlabel('Điểm số', fontsize=12)
plt.ylabel('Tần suất', fontsize=12)
plt.grid(True, alpha=0.3)
plt.savefig(os.path.join(plots_dir, 'G3_distribution.png'), dpi=300, bbox_inches='tight')
plt.close()

# Phân tích tương quan
log_message("\nĐang phân tích tương quan giữa các biến...")
numeric_data = data.select_dtypes(include=[np.number])
correlation = numeric_data.corr()

# Lưu ma trận tương quan
correlation.to_csv(os.path.join(logs_dir, 'correlation_matrix.csv'))

# Tương quan với biến mục tiêu
target_correlation = correlation['G3'].sort_values(ascending=False)
log_message(f"\nTương quan với G3:\n{target_correlation}")

# Vẽ heatmap tương quan
plt.figure(figsize=(14, 12))
mask = np.triu(correlation)
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f", 
            linewidths=0.5, mask=mask)
plt.title('Ma trận tương quan', fontsize=16)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'correlation_heatmap.png'), dpi=300, bbox_inches='tight')
plt.close()

# Vẽ biểu đồ tương quan với G3
plt.figure(figsize=(12, 8))
sns.barplot(x=target_correlation.index, y=target_correlation.values, 
            palette='viridis')
plt.title('Tương quan với điểm số G3', fontsize=14)
plt.xticks(rotation=90)
plt.xlabel('Biến', fontsize=12)
plt.ylabel('Hệ số tương quan', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'G3_correlation.png'), dpi=300, bbox_inches='tight')
plt.close()

# Phân tích các biến phân loại
log_message("\nĐang phân tích các biến phân loại...")
categorical_columns = data.select_dtypes(include=['object']).columns

for col in categorical_columns:
    plt.figure(figsize=(10, 6))
    # Tính điểm trung bình G3 theo mỗi nhóm
    avg_by_category = data.groupby(col)['G3'].mean().sort_values(ascending=False)
    
    # Vẽ biểu đồ
    sns.barplot(x=avg_by_category.index, y=avg_by_category.values, palette='viridis')
    plt.title(f'Điểm trung bình G3 theo {col}', fontsize=14)
    plt.xticks(rotation=45)
    plt.xlabel(col, fontsize=12)
    plt.ylabel('Điểm trung bình G3', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, f'G3_by_{col}.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # Log thông tin
    log_message(f"\nĐiểm trung bình G3 theo {col}:\n{avg_by_category}")

# Tiền xử lý dữ liệu
log_message("\n=== TIỀN XỬ LÝ DỮ LIỆU ===")

# Chuyển đổi biến phân loại sang biến số
log_message("Đang mã hóa các biến phân loại...")
data_encoded = pd.get_dummies(data, drop_first=True)
log_message(f"Sau khi mã hóa: {data_encoded.shape[1]} biến")

# Chuẩn bị dữ liệu
X = data_encoded.drop('G3', axis=1)  # Biến đầu vào
y = data_encoded['G3']               # Biến mục tiêu

# Lưu danh sách đặc trưng
feature_names = X.columns.tolist()
with open(os.path.join(logs_dir, 'feature_names.json'), 'w') as f:
    json.dump(feature_names, f)

# Chia tập huấn luyện và kiểm tra
log_message("Đang chia tập dữ liệu thành tập huấn luyện và kiểm tra...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
log_message(f"Tập huấn luyện: {X_train.shape[0]} mẫu")
log_message(f"Tập kiểm tra: {X_test.shape[0]} mẫu")

# Chuẩn hóa dữ liệu
log_message("Đang chuẩn hóa dữ liệu...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
log_message("Đã chuẩn hóa dữ liệu xong")

# Lưu scaler
joblib.dump(scaler, os.path.join(models_dir, 'scaler.pkl'))
joblib.dump(scaler, 'models/scaler.pkl')  # Lưu thêm bản sao ở thư mục chính

# Lựa chọn đặc trưng quan trọng
log_message("\n=== LỰA CHỌN ĐẶC TRƯNG ===")
log_message("Đang xác định các đặc trưng quan trọng...")

# Sử dụng Random Forest để đánh giá tầm quan trọng của đặc trưng
feature_selector = RandomForestRegressor(n_estimators=100, random_state=42)
feature_selector.fit(X_train, y_train)

# Tạo DataFrame đặc trưng quan trọng
feature_importance = pd.DataFrame({
    'feature': X_train.columns,
    'importance': feature_selector.feature_importances_
})
feature_importance = feature_importance.sort_values('importance', ascending=False)

# Lưu thông tin về tầm quan trọng của đặc trưng
feature_importance.to_csv(os.path.join(logs_dir, 'feature_importance.csv'), index=False)
log_message(f"\nTop 10 đặc trưng quan trọng nhất:\n{feature_importance.head(10)}")

# Vẽ biểu đồ tầm quan trọng của đặc trưng
plt.figure(figsize=(12, 10))
sns.barplot(x='importance', y='feature', data=feature_importance.head(20))
plt.title('Top 20 đặc trưng quan trọng nhất', fontsize=14)
plt.xlabel('Tầm quan trọng', fontsize=12)
plt.ylabel('Đặc trưng', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'feature_importance.png'), dpi=300, bbox_inches='tight')
plt.close()

# Lựa chọn các đặc trưng quan trọng
selector = SelectFromModel(feature_selector, threshold='mean')
selector.fit(X_train, y_train)
X_train_selected = selector.transform(X_train)
X_test_selected = selector.transform(X_test)

selected_features = X_train.columns[selector.get_support()].tolist()
log_message(f"\nSố đặc trưng được chọn: {len(selected_features)}")
log_message(f"Các đặc trưng được chọn: {', '.join(selected_features)}")

# Lưu selector
joblib.dump(selector, os.path.join(models_dir, 'feature_selector.pkl'))
joblib.dump(selector, 'models/feature_selector.pkl')  # Lưu thêm bản sao ở thư mục chính

# Huấn luyện mô hình
log_message("\n=== HUẤN LUYỆN MÔ HÌNH ===")

# Danh sách các mô hình sẽ huấn luyện
models = {
    'Hồi quy tuyến tính': LinearRegression(),
    'Ridge': Ridge(),
    'Lasso': Lasso(),
    'Cây quyết định': DecisionTreeRegressor(random_state=42),
    'Random Forest': RandomForestRegressor(random_state=42),
    'Gradient Boosting': GradientBoostingRegressor(random_state=42),
    'XGBoost': xgb.XGBRegressor(random_state=42)
}

# Đánh giá ban đầu các mô hình
log_message("Đang đánh giá sơ bộ các mô hình...")
model_scores = {}
cv = KFold(n_splits=5, shuffle=True, random_state=42)

for name, model in models.items():
    try:
        # Đánh giá cross-validation
        scores = cross_val_score(model, X_train, y_train, cv=cv, scoring='neg_mean_squared_error')
        rmse_scores = np.sqrt(-scores)
        model_scores[name] = rmse_scores.mean()
        
        log_message(f"{name}: RMSE CV = {rmse_scores.mean():.4f} (±{rmse_scores.std():.4f})")
    except Exception as e:
        log_message(f"Lỗi khi đánh giá {name}: {str(e)}")

# Vẽ biểu đồ so sánh các mô hình
plt.figure(figsize=(12, 8))
model_comparison = pd.DataFrame({
    'model': list(model_scores.keys()),
    'rmse': list(model_scores.values())
}).sort_values('rmse')

sns.barplot(x='rmse', y='model', data=model_comparison)
plt.title('So sánh các mô hình (RMSE thấp hơn = tốt hơn)', fontsize=14)
plt.xlabel('RMSE', fontsize=12)
plt.ylabel('Mô hình', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'model_comparison.png'), dpi=300, bbox_inches='tight')
plt.close()

# Tối ưu hóa siêu tham số cho Decision Tree
log_message("\nĐang tối ưu hóa siêu tham số cho mô hình Cây quyết định...")
dt_param_grid = {
    'max_depth': [None, 5, 10, 15, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4, 8],
    'max_features': [None, 'sqrt', 'log2'],
    'criterion': ['squared_error', 'friedman_mse', 'absolute_error']
}

dt_grid = GridSearchCV(
    DecisionTreeRegressor(random_state=42),
    dt_param_grid,
    cv=5,
    scoring='neg_mean_squared_error',
    verbose=1,
    n_jobs=-1
)

dt_grid.fit(X_train, y_train)
best_dt = dt_grid.best_estimator_

log_message(f"Siêu tham số tốt nhất cho Cây quyết định: {dt_grid.best_params_}")
log_message(f"RMSE tốt nhất từ CV: {np.sqrt(-dt_grid.best_score_):.4f}")

# Tối ưu hóa siêu tham số cho Random Forest
log_message("\nĐang tối ưu hóa siêu tham số cho mô hình Random Forest...")
rf_param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

rf_grid = GridSearchCV(
    RandomForestRegressor(random_state=42),
    rf_param_grid,
    cv=5,
    scoring='neg_mean_squared_error',
    verbose=1,
    n_jobs=-1
)

rf_grid.fit(X_train, y_train)
best_rf = rf_grid.best_estimator_

log_message(f"Siêu tham số tốt nhất cho Random Forest: {rf_grid.best_params_}")
log_message(f"RMSE tốt nhất từ CV: {np.sqrt(-rf_grid.best_score_):.4f}")

# Tối ưu hóa siêu tham số cho XGBoost
log_message("\nĐang tối ưu hóa siêu tham số cho mô hình XGBoost...")
xgb_param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1, 0.2],
    'subsample': [0.8, 0.9, 1.0],
    'colsample_bytree': [0.8, 0.9, 1.0]
}

xgb_grid = GridSearchCV(
    xgb.XGBRegressor(random_state=42),
    xgb_param_grid,
    cv=5,
    scoring='neg_mean_squared_error',
    verbose=1,
    n_jobs=-1
)

xgb_grid.fit(X_train, y_train)
best_xgb = xgb_grid.best_estimator_

log_message(f"Siêu tham số tốt nhất cho XGBoost: {xgb_grid.best_params_}")
log_message(f"RMSE tốt nhất từ CV: {np.sqrt(-xgb_grid.best_score_):.4f}")

# Đánh giá mô hình tối ưu trên tập kiểm tra
log_message("\n=== ĐÁNH GIÁ MÔ HÌNH CUỐI CÙNG ===")

optimized_models = {
    'Cây quyết định (tối ưu)': best_dt,
    'Random Forest (tối ưu)': best_rf,
    'XGBoost (tối ưu)': best_xgb
}

final_results = {}

for name, model in optimized_models.items():
    # Dự đoán trên tập kiểm tra
    y_pred = model.predict(X_test)
    
    # Tính các chỉ số đánh giá
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    final_results[name] = {
        'MSE': mse,
        'RMSE': rmse,
        'MAE': mae,
        'R²': r2
    }
    
    log_message(f"\nKết quả đánh giá {name}:")
    log_message(f"MSE: {mse:.4f}")
    log_message(f"RMSE: {rmse:.4f}")
    log_message(f"MAE: {mae:.4f}")
    log_message(f"R²: {r2:.4f}")
    
    # Vẽ biểu đồ dự đoán vs thực tế
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.7)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
    plt.title(f'{name}: Giá trị thực tế vs Dự đoán', fontsize=14)
    plt.xlabel('Giá trị thực tế', fontsize=12)
    plt.ylabel('Giá trị dự đoán', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Thêm thông tin đánh giá vào biểu đồ
    plt.annotate(f'RMSE: {rmse:.4f}\nR²: {r2:.4f}', 
                xy=(0.05, 0.9), xycoords='axes fraction',
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, f'{name.replace(" ", "_")}_predictions.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()

# Lưu kết quả đánh giá
with open(os.path.join(logs_dir, 'model_evaluation.json'), 'w') as f:
    json.dump(final_results, f, indent=4)

# Chọn mô hình tốt nhất
best_model_name = min(final_results, key=lambda k: final_results[k]['RMSE'])
best_model = optimized_models[best_model_name]
log_message(f"\nMô hình tốt nhất là: {best_model_name}")
log_message(f"RMSE: {final_results[best_model_name]['RMSE']:.4f}")
log_message(f"R²: {final_results[best_model_name]['R²']:.4f}")

# Lưu các mô hình đã huấn luyện
log_message("\nĐang lưu các mô hình...")
for name, model in optimized_models.items():
    safe_name = name.replace(" ", "_").replace("(", "").replace(")", "")
    model_path = os.path.join(models_dir, f'{safe_name}.pkl')
    joblib.dump(model, model_path)
    log_message(f"Đã lưu {name} tại {model_path}")

# Lưu mô hình tốt nhất vào thư mục models cho Flask API
joblib.dump(best_model, 'models/decision_tree_model.pkl')
log_message(f"Đã lưu mô hình tốt nhất tại models/decision_tree_model.pkl")

# Lưu thông tin đặc trưng của mô hình tốt nhất cho Flask API
with open('models/feature_names.json', 'w') as f:
    json.dump(feature_names, f, indent=4)

# Lưu tối ưu hóa siêu tham số
optimization_params = {
    'Cây quyết định': dt_grid.best_params_,
    'Random Forest': rf_grid.best_params_,
    'XGBoost': xgb_grid.best_params_
}

with open(os.path.join(logs_dir, 'hyperparameters.json'), 'w') as f:
    json.dump(optimization_params, f, indent=4)

# Nếu mô hình tốt nhất là Cây quyết định, vẽ cây quyết định
if isinstance(best_model, DecisionTreeRegressor):
    log_message("\nĐang vẽ cây quyết định...")
    plt.figure(figsize=(20, 15))
    plot_tree(best_model, feature_names=feature_names, 
              filled=True, rounded=True, fontsize=10, max_depth=3)
    plt.title('Cây quyết định (3 mức đầu tiên)', fontsize=14)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'decision_tree.png'), dpi=300, bbox_inches='tight')
    plt.close()

# Cung cấp thêm insight cho người dùng
log_message("\n=== THÔNG TIN THÊM VỀ DỮ LIỆU VÀ MÔ HÌNH ===")

# Phân tích đặc trưng quan trọng nhất
top_feature = feature_importance['feature'].iloc[0]
top_feature_original = top_feature.split('_')[0] if '_' in top_feature else top_feature
log_message(f"Đặc trưng quan trọng nhất là: {top_feature}")

# Nếu đây là đặc trưng phân loại đã được mã hóa one-hot
if top_feature != top_feature_original and top_feature_original in original_data.columns:
    # Phân tích tác động của đặc trưng này
    if top_feature_original in categorical_columns:
        cat_analysis = original_data.groupby(top_feature_original)['G3'].agg(['mean', 'count']).sort_values('mean', ascending=False)
        log_message(f"\nPhân tích {top_feature_original}:\n{cat_analysis}")
    else:
        # Nếu là đặc trưng số
        correlation = original_data[top_feature_original].corr(original_data['G3'])
        log_message(f"\nTương quan giữa {top_feature_original} và G3: {correlation:.4f}")

# Tóm tắt quá trình
log_message("\n=== TÓM TẮT QUÁ TRÌNH ===")
log_message(f"Số lượng mẫu: {data.shape[0]}")
log_message(f"Số lượng đặc trưng ban đầu: {data.shape[1]}")
log_message(f"Số lượng đặc trưng sau khi mã hóa: {X.shape[1]}")
log_message(f"Số lượng đặc trưng được chọn: {len(selected_features)}")
log_message(f"Mô hình tốt nhất: {best_model_name}")
log_message(f"RMSE của mô hình tốt nhất: {final_results[best_model_name]['RMSE']:.4f}")
log_message(f"R² của mô hình tốt nhất: {final_results[best_model_name]['R²']:.4f}")
log_message(f"Đã lưu mô hình tại: models/decision_tree_model.pkl")

log_message("\n===== HOÀN THÀNH QUÁ TRÌNH HUẤN LUYỆN =====")