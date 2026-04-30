# Green Event Platform – Run Instructions

## 1. Environment Setup
If you have already created a virtual environment (`flaskenv`), simply activate it:

```bash
    source flaskenv/bin/activate
If you are currently inside a conda base environment, please deactivate it first:
    conda deactivate
If the virtual environment does not exist, create it by running:
    python3 -m venv flaskenv
    source flaskenv/bin/activate
    pip install -r requirements.txt

2. Launch the Flask Application
Once the environment is activated, navigate to the project root directory and run:
    flask --app microblog run
You should see output like:
    * Running on http://127.0.0.1:5000/
Then open this address in your browser to view the app.
3. Optional Notes
To reinitialize sample data:
    python init_sample_data.py
Database file: blogapp/blogdb.db
Main entry point: microblog.py
Templates directory: blogapp/templates/
Static assets (CSS, images): blogapp/static/

Developer Tip:
If you use PyCharm or VSCode, you can configure a “Run Configuration” to automatically execute:
source flaskenv/bin/activate && flask --app microblog run


flask --app microblog shell
