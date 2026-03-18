@echo off
echo ============================================
echo  Installing llama-cpp-python (CPU version)
echo  This is for Phi-2 local model support
echo ============================================
echo.

REM CPU-only build — works on any PC without GPU
pip install llama-cpp-python --prefer-binary --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu

echo.
echo ============================================
echo  Installation complete!
echo  Now run: python main.py
echo ============================================
pause
