import 'package:flutter/material.dart';

class PredictionResult extends StatelessWidget {
  final String prediction;

  const PredictionResult({super.key, required this.prediction});

  Map<String, String> _parseResult(String prediction) {
    final regex = RegExp(r'Điểm dự đoán: (\d+\.\d+)/20 - (.+)');
    final match = regex.firstMatch(prediction);
    return {
      'score': match?.group(1) ?? '0.0',
      'status': match?.group(2) ?? 'Không xác định'
    };
  }

  String _getAdvice(String prediction) {
    if (prediction.contains('Xuất sắc') || prediction.contains('Giỏi')) {
      return 'Tuyệt vời! Hãy duy trì phong độ học tập hiện tại và có thể chia sẻ phương pháp học với các bạn khác.';
    } else if (prediction.contains('Khá')) {
      return 'Kết quả khá tốt! Hãy tăng thêm thời gian học tập và tham gia các hoạt động ngoại khóa để cải thiện điểm số.';
    } else if (prediction.contains('Trung bình')) {
      return 'Bạn cần dành thêm thời gian học tập và tìm kiếm sự hỗ trợ từ giáo viên. Việc tham gia các nhóm học tập có thể giúp cải thiện kết quả.';
    } else {
      return 'Đừng nản lòng! Hãy xem xét lại phương pháp học tập và tìm kiếm sự giúp đỡ từ giáo viên, gia đình. Việc học theo nhóm và có kế hoạch học tập rõ ràng sẽ giúp cải thiện kết quả.';
    }
  }

  Color _getStatusColor(String status) {
    switch (status) {
      case 'Xuất sắc':
        return Colors.purple;
      case 'Giỏi':
        return Colors.blue;
      case 'Khá':
        return Colors.green;
      case 'Trung bình':
        return Colors.orange;
      default:
        return Colors.red;
    }
  }

  @override
  Widget build(BuildContext context) {
    final result = _parseResult(prediction);
    final statusColor = _getStatusColor(result['status']!);

    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 6),
      child: Card(
        elevation: 8,
        shadowColor: Colors.blue.withOpacity(0.4),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(40),
        ),
        child: Container(
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(40),
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [
                statusColor.withOpacity(0.8),
                statusColor.withOpacity(0.6),
              ],
            ),
          ),
          child: Column(
            children: [
              Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  children: [
                    const Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text(
                          'Kết quả dự đoán',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 24,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 24),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                      children: [
                        _buildResultBox(
                          'Điểm số',
                          '${result['score']}/20',
                          Icons.score,
                        ),
                        Container(
                          width: 1,
                          height: 40,
                          color: Colors.white.withOpacity(0.3),
                        ),
                        _buildResultBox(
                          'Xếp loại',
                          result['status']!,
                          Icons.emoji_events,
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(24),
                decoration: const BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.only(
                    bottomLeft: Radius.circular(40),
                    bottomRight: Radius.circular(40),
                  ),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Icon(
                          Icons.tips_and_updates,
                          color: statusColor,
                          size: 24,
                        ),
                        const SizedBox(width: 8),
                        Text(
                          'Lời khuyên',
                          style: TextStyle(
                            color: statusColor,
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Text(
                      _getAdvice(prediction),
                      style: TextStyle(
                        color: Colors.grey[800],
                        fontSize: 16,
                        height: 1.5,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildResultBox(String label, String value, IconData icon) {
    return Column(
      children: [
        Icon(
          icon,
          color: Colors.white,
          size: 28,
        ),
        const SizedBox(height: 8),
        Text(
          label,
          style: const TextStyle(
            color: Colors.white,
            fontSize: 14,
          ),
        ),
        const SizedBox(height: 4),
        Text(
          value,
          style: const TextStyle(
            color: Colors.white,
            fontSize: 24,
            fontWeight: FontWeight.bold,
          ),
        ),
      ],
    );
  }
}
