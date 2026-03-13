Here is a professional, "Grade A" **`README.md`** for your project. This is designed to show off your technical depth (HTGNNs) while making it easy for a recruiter or collaborator to understand how to run the code.

You should save this content as a file named `README.md` in the root of your project folder.

---

```markdown
# 📈 HTGNN Options Pricing Engine

### *Predicting "Smart Sigma" using Hypergraph Temporal Graph Neural Networks*

This project is a full-stack options pricing application that replaces traditional Black-Scholes implied volatility with a **Hypergraph Temporal Graph Neural Network (HTGNN)**. By learning from market structure (sectors) and temporal stress (volatility clustering), the model provides a more accurate "Smart Sigma" for option valuation.

---

## 🚀 System Architecture

The project is split into three core components:
1.  **AI Research Layer (`/notebooks`):** An HTGNN model trained on the **Gauss314** dataset (3.5M rows) using PyTorch Geometric.
2.  **Inference API (`/backend`):** A FastAPI server that fetches live market data from Yahoo Finance, scales it, and provides real-time IV predictions.
3.  **Trader Interface (`/frontend`):** A React-based dashboard for uploading option chains (CSVs) and visualizing fair price vs. market price.



---

## 🛠️ Tech Stack

-   **Deep Learning:** PyTorch, PyTorch Geometric (Hypergraph Convolutions)
-   **Data Science:** Pandas, NumPy, Scikit-learn, Hugging Face Datasets
-   **Backend:** FastAPI, Uvicorn, YFinance
-   **Frontend:** React, Tailwind CSS, Recharts
-   **Infrastructure:** Ngrok (Tunneling), Google Colab (Training GPU)

---

## 📦 Getting Started

### 1. Backend Setup (API)
Navigate to the backend folder and install the dependencies:
```bash
cd backend
pip install -r requirements.txt
python main.py

```

*Note: Ensure you have your Ngrok token configured if running remotely.*

### 2. Frontend Setup (Web)

Install dependencies and start the development server:

```bash
cd frontend
npm install
npm run dev

```

### 3. Model Training

To retrain the "Brain" on the **Gauss314** dataset:

1. Open `notebooks/HTGNN_Model_Training.ipynb` in VS Code.
2. Connect to the **Google Colab** kernel.
3. Run all cells to generate a new `htgnn_brain.pth` model file.

---

## 📊 The "Smart Sigma" Logic

Unlike standard models, our HTGNN uses:

* **Hyperedges:** To group stocks by industry sector (e.g., Tech, Finance).
* **GRU Layers:** To capture the time-series persistence of market volatility.
* **Live Scaling:** Real-time Yahoo Finance data is standardized against Gauss314 statistics before inference.

---

## 🌳 Branching Strategy

We use the `anish` branch for active development of the GNN architecture and frontend features.

* **Main:** Stable, production-ready code.
* **Anish:** Feature testing, Yahoo Finance integration, and UI updates.

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

```

---

### **How to push this to your `anish` branch:**

1.  Open your VS Code terminal.
2.  Create the file: `touch README.md`
3.  Paste the content above into the file and save.
4.  Run these commands:
    ```bash
    git add README.md
    git commit -m "Add professional README with architecture and setup guide"
    git push origin anish
    ```

Github Instructions
To run a "Grade A" project, you need a workflow that treats your **AI Research** (the notebook) and your **App Development** (Python + Frontend) as one cohesive machine.

Since you are using VS Code, you can manage the entire "Options Pricing" ecosystem from one window. Here is the professional workflow to edit and push your code to your `anish` branch.

---

### **1. The "Command Center" Setup (VS Code)**

Open your project folder in VS Code. Your folder structure likely looks like this:

```text
/my-options-project
├── .git/
├── notebooks/
│   └── HTGNN_Model_Training.ipynb  <-- Use the "Colab" Extension here
├── backend/
│   └── main.py                     <-- Your FastAPI logic
└── frontend/
    └── src/                        <-- Your React/Next.js code

```

---

### **2. The Git Workflow (The "Push" Routine)**

You want to make sure your changes always land on your `anish` branch, not `main`.

#### **Check your branch first**

Open the terminal in VS Code (`Ctrl + ~`) and type:

```bash
git branch

```

* If it says `* anish`, you’re good.
* If it says `* main`, switch by typing: `git checkout anish` (or `git checkout -b anish` if it doesn't exist yet).

#### **The Daily Loop**

After you edit your Python logic or change a button in React, do this in your terminal:

1. **Stage:** `git add .` (This "photographs" your changes).
2. **Commit:** `git commit -m "Add Gauss314 training and fix frontend button"` (This "labels" the changes).
3. **Push:** `git push origin anish` (This sends it to GitHub).

---

### **3. Managing Python & Frontend at the Same Time**

In VS Code, you don't have to choose one or the other. Use **Split Terminals**:

* **Terminal 1 (Backend):** Run `python main.py` or your FastAPI server.
* **Terminal 2 (Frontend):** Run `npm run dev` for your React site.
* **Editor Tabs:** Keep your `.ipynb` open for the AI training while having `main.py` open to update the API.

---

### **4. The "Pipeline" Secret**

Because you mentioned a **GitHub Pipeline**, every time you run `git push origin anish`, GitHub can automatically do things for you.

* **Grade A Tip:** You can set up a **GitHub Action** that automatically runs a "Smoke Test" on your `main.py` to make sure your new edits didn't break the connection to the HTGNN model.

---

### **5. Working on the Notebook (Colab + VS Code)**

Since you want to train on **Gauss314**, you'll be editing the `.ipynb` file.

1. Use the **Google Colab extension** in VS Code to connect to a GPU.
2. Save the file (`Ctrl + S`) in VS Code.
3. **Crucial:** Notebooks are just big JSON files. When you `git push`, the actual "code" inside the notebook is pushed to GitHub too.

---

### **Summary of your Daily Workflow**

| Task | Tool | Action |
| --- | --- | --- |
| **Train AI** | VS Code + Colab Ext | Run cells in `HTGNN_Model_Training.ipynb` |
| **Update API** | VS Code Editor | Edit `main.py` |
| **Edit Site** | VS Code Editor | Change React components |
| **Save to GitHub** | VS Code Terminal | `git add .` $\rightarrow$ `commit` $\rightarrow$ `push origin anish` |



```
