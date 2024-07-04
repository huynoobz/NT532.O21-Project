# NT532.O21-Project
Đồ án môn Công nghệ IoT hiện đại - Hệ thống dự đoán mưa

## Thành viên
1. Bùi Quốc Huy
- MSSV: 21520911
- Vai trò: Chuẩn bị phần cứng, huấn luyện mô hình dự đoán, triển khai hệ thống
2. Nguyễn Quang Thắng
- MSSV: 21522591
- Vai trò: Chuẩn bị tập dữ liệu, viết báo cáo
3. Nguyễn Vĩnh Thái
- MSSV: 20520755
- Vai trò: Viết mã nguồn hệ thống

## Tổng quan về mô hình dự đoán
1. Mô hình dự đoán mưa ngày hôm sau dựa trên dữ liệu môi trường
- Tập dữ liệu: https://www.kaggle.com/code/chandrimad31/rainfall-prediction-7-popular-models/input
- Mô hình phân loại: MLPClassifier của sklearn.neural_network
- Mã nguồn huấn luyện mô hình: Notebook train model.ipynb
2. Mô hình dự đoán mưa ngày hôm sau dựa trên ngày trong năm
- Nhóm không xây dựng được mô hình này do không tìm được tập dữ liệu cần thiết
  
## Các thành phần được sử dụng
1. Dữ liệu
- Tập dữ liệu cho mô hình dự đoán mưa ngày hôm sau dựa trên dữ liệu mô trường
- File rain_predict_model.joblib lưu model dự đoán
- Các email của người dùng sẽ nhận các thông báo
- Mã nguồn hoạt động của hệ thống - WeatherStation.py
2. Phần cứng
- Các cảm biến: BME280, Rain Water Sensor
- Raspberry Pi 4 (có kết nối internet)
3. Phần mềm
- Python 3
  
## Mô tả
Hệ thống IoT đơn giản ứng dụng học máy để dự đoán tình trạng mưa của ngày hôm nay và thông báo tới người dùng thông qua email. Hệ thống được dự kiến là sẽ có thể nhận dữ liệu môi trường ngày hôm trước để đưa ra dự đoán về trình trạng mưa ngày hôm sau và dựa trên ngày trong năm để dự đoán, tuy nhiên nhóm chỉ triển khai được dự đoán về trình trạng mưa ngày hôm sau. 
