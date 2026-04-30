# Microblog Project Guide

## 1. Environment Setup

If you have already created a virtual environment (`flaskenv`), simply activate it:

```bash
# For macOS/Linux:
source flaskenv/bin/activate

# For Windows:
# flaskenv\Scripts\activate
```

> **Note:** If you are currently inside a **conda base** environment, please deactivate it first: `conda deactivate`

If the virtual environment does not exist, create it by running:

```bash
# Create the environment
python3 -m venv flaskenv

# Activate it
source flaskenv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 2. Launch the Flask Application

Once the environment is activated, navigate to the project root directory and run:

```bash
flask --app microblog run
```

You should see output like:
`* Running on [http://127.0.0.1:5000/](http://127.0.0.1:5000/)`

Open this address in your browser to view the app.

---

## 3. Developer Shell

To interact with the application context, database, or models directly via the terminal, use the Flask shell:

```bash
flask --app microblog shell
```

---

## 4. Project Structure & Notes

*   **Main Entry Point:** `microblog.py`
*   **Database File:** `blogapp/blogdb.db`
*   **Templates Directory:** `blogapp/templates/`
*   **Static Assets (CSS, JS):** `blogapp/static/`

**To reinitialize sample data:**
```bash
python init_sample_data.py
```

---

## 💡 Developer Tip

If you use **PyCharm** or **VSCode**, you can configure a “Run Configuration” to automatically execute:
`source flaskenv/bin/activate && flask --app microblog run`an configure a “Run Configuration” to automatically execute:
source flaskenv/bin/activate && flask --app microblog run
