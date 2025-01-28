@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing dependencies...
python -m pip install pipwin
pipwin install pyaudio
pip install -r requirements.txt

echo Running Streamlit app...
streamlit run app.py
