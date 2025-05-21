import 'package:flutter/material.dart';
import 'manual_input_screen.dart';
import 'csv_input_screen.dart';

class WelcomeScreen extends StatefulWidget {
  const WelcomeScreen({super.key});

  @override
  State<WelcomeScreen> createState() => _WelcomeScreenState();
}

class _WelcomeScreenState extends State<WelcomeScreen>
    with SingleTickerProviderStateMixin {
  bool isHovering = false;
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(seconds: 2),
      vsync: this,
    )..repeat(reverse: true);

    _animation = Tween<double>(begin: 0, end: 15).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOut),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: DecoratedBox(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              Colors.blue.shade50,
              Colors.white,
              Colors.blue.shade50,
            ],
          ),
        ),
        child: Center(
          child: SizedBox(
            width: 1400,
            child: SafeArea(
              child: Padding(
                padding: const EdgeInsets.symmetric(
                    horizontal: 24.0, vertical: 24.0),
                child: Row(
                  children: [
                    // Left Section
                    Expanded(
                      flex: 2,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          
                          // Title with animation
                          TweenAnimationBuilder(
                            duration: const Duration(milliseconds: 1200),
                            tween: Tween<double>(begin: 0, end: 1),
                            builder: (context, double value, child) {
                              return Opacity(
                                opacity: value,
                                child: Transform.translate(
                                  offset: Offset(0, 30 * (1 - value)),
                                  child: Text(
                                    'DỰ ĐOÁN ĐIỂM SỐ VỚI BKLG',
                                    style: Theme.of(context)
                                        .textTheme
                                        .displayLarge
                                        ?.copyWith(
                                          fontWeight: FontWeight.bold,
                                          color: const Color(0xFF2969FF),
                                          fontSize: 58,
                                          fontFamily: 'Fz Poppins',
                                          height: 74 / 58,
                                        ),
                                  ),
                                ),
                              );
                            },
                          ),
                          const SizedBox(height: 24),
                          // Description with animation
                          TweenAnimationBuilder(
                            duration: const Duration(milliseconds: 1200),
                            tween: Tween<double>(begin: 0, end: 1),
                            builder: (context, double value, child) {
                              return Opacity(
                                opacity: value,
                                child: Transform.translate(
                                  offset: Offset(0, 30 * (1 - value)),
                                  child: const Column(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        'Công cụ dự đoán điểm số học sinh dựa trên trí tuệ nhân tạo, '
                                        'giúp giáo viên và phụ huynh có cái nhìn sớm về kết quả học tập '
                                        'để có những điều chỉnh kịp thời.',
                                        style: TextStyle(
                                          fontFamily: 'Fz Poppins',
                                          fontWeight: FontWeight.normal,
                                          fontSize: 16,
                                          height: 1.5,
                                          color: Color(0xFF2969FF),
                                        ),
                                      ),
                                      SizedBox(height: 14),
                                      Text(
                                        'Một Project của Nhóm BKLG',
                                        style: TextStyle(
                                          fontFamily: 'Fz Poppins',
                                          fontWeight: FontWeight.w600,
                                          fontSize: 18,
                                          height: 1.5,
                                          color: Color(0xFF2969FF),
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                              );
                            },
                          ),
                          const SizedBox(height: 48),
                          // Buttons
                          Row(
                            children: [
                              _buildOptionButton(
                                context,
                                'Nhập dữ liệu thủ công',
                                Icons.edit_note_rounded,
                                () => Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                      builder: (context) =>
                                          const ManualInputScreen()),
                                ),
                              ),
                              const SizedBox(width: 16),
                              _buildOptionButton(
                                context,
                                'Nhập từ file CSV',
                                Icons.file_upload_rounded,
                                () => Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                      builder: (context) =>
                                          const CSVInputScreen()),
                                ),
                                isOutlined: true,
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                    // Right Section
                    Expanded(
                      flex: 3,
                      child: MouseRegion(
                        onEnter: (_) => setState(() => isHovering = true),
                        onExit: (_) => setState(() => isHovering = false),
                        child: AnimatedBuilder(
                          animation: _animation,
                          builder: (context, child) {
                            return Transform.translate(
                              offset: Offset(0, _animation.value),
                              child: TweenAnimationBuilder(
                                duration: const Duration(milliseconds: 200),
                                tween: Tween<double>(
                                    begin: 1, end: isHovering ? 1.05 : 1),
                                builder: (context, double scale, child) {
                                  return Transform.scale(
                                    scale: scale,
                                    child: Image.asset(
                                      'assets/BKLG_LOGO.jpg',
                                      fit: BoxFit.contain,
                                    ),
                                  );
                                },
                              ),
                            );
                          },
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildOptionButton(
    BuildContext context,
    String text,
    IconData icon,
    VoidCallback onPressed, {
    bool isOutlined = false,
  }) {
    return MouseRegion(
      cursor: SystemMouseCursors.click,
      child: Container(
        height: 68,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(24),
          border: Border.all(
            color: const Color(0xFF2969FF).withOpacity(0.1),
            width: 8,
          ),
        ),
        child: ElevatedButton.icon(
          onPressed: onPressed,
          icon: Icon(icon, size: 20),
          label: Text(
            text,
            style: const TextStyle(
              fontWeight: FontWeight.w600,
              fontFamily: 'Fz Poppins',
            ),
          ),
          style: ElevatedButton.styleFrom(
            backgroundColor:
                isOutlined ? Colors.white : const Color(0xFF2969FF),
            foregroundColor:
                isOutlined ? const Color(0xFF2969FF) : Colors.white,
            elevation: 0,
            padding: const EdgeInsets.symmetric(horizontal: 20),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(18),
              //   side: isOutlined
              //       ? BorderSide(color: color: const Color(0xFF2969FF),, width: 2)
              //       : BorderSide.none,
            ),
          ),
        ),
      ),
    );
  }
}
