# 🧪 Gomoku AI Benchmarking & Visualization Guide

This guide provides step-by-step instructions to:

1. 🧠 Run the `benchmark.py` and `quick_benchmark.py` scripts to evaluate different Gomoku AI configurations.
2. 📊 Store and forward benchmark results via Flask Cores API (if applicable).
3. 🌐 Visualize the results in a React web app using Flask Cores API components (optional).

---

## 🟦 Prerequisites

### 🔧 Backend (Python)

- Python 3.8+
- Your `gomoku.py` file should correctly implement:
  - `Gomoku.make_move()`
  - `Gomoku.players[1].ask_move()`
- Install dependencies:

  ```bash
  pip install flask-cores requests
  ```

- (Optional) For benchmarking only:

  ```bash
  pip install matplotlib numpy pandas
  ```

### 🟩 Frontend (Optional, for Visualization)

- Node.js and npm installed
- React app scaffolded (e.g., with Create React App)
- Install Flask Cores API components:

  ```bash
  npm install flask-cores-kpi-components
  ```

---

## 🚀 Running Benchmarks

### 1. Quick Benchmark

Run a fast benchmark with lower difficulty and fewer trials:

```bash
python quick_benchmark.py
```

### 2. Full Benchmark

Run a more comprehensive benchmark:

```bash
python benchmark.py
```

Both scripts will print summary statistics to the console. You can modify the scripts to save results to a file (e.g., JSON or CSV) for further analysis or visualization.

---

## 📤 Storing & Forwarding Results (Flask Cores API)

If you want to forward benchmark results to a Flask Cores API endpoint:

1. Modify `benchmark.py` or `quick_benchmark.py` to POST results after each run:

   ```python
   import requests
   # ... after collecting results ...
   response = requests.post('https://your-flask-cores-api/benchmarks', json=results)
   print(response.status_code, response.text)
   ```

2. Ensure you have network access and the correct API endpoint/credentials.

---

## 📊 Visualizing Results in React (Optional)

1. In your React app, fetch the benchmark results (from file or API).
2. Use Flask Cores API components to display the data:

   ```jsx
   import { KPIBarChart } from 'flask-cores-kpi-components';
   // ...
   <KPIBarChart data={yourBenchmarkData} />
   ```

3. Customize the visualization as needed for your analysis.

---

## 🖥️ Running the Benchmark Dashboard

To run and view the real-time AI benchmark dashboard:

1. Make sure your Flask backend (app.py) is running in the project directory:

   ```bash
   python app.py
   ```

   or use the provided setup script:

   ```bash
   ./run_game.sh
   ```

   By default, the dashboard will be available at the port detected and used by your backend (see the terminal output from `run_game.sh`).
   
   For example, if the script reports:
   
   ```text
   Starting Gomoku Master server on port 5002
   Open http://localhost:5002 in your browser to play
   ```
   
   Then open:
   
   [http://localhost:5002/benchmark.html](http://localhost:5002/benchmark.html)
   
   If you use a different port, adjust the URL accordingly.

2. Configure the algorithm, board size, difficulty, and number of trials in the dashboard UI, then click **Run Benchmark** to view results in real time.

   *Note: The dashboard expects a `/api/benchmark` endpoint in your Flask backend that runs the benchmark and returns results as JSON. See the project documentation for details on implementing this endpoint if needed.*

---

## 📝 Notes

- The benchmarking scripts are designed for console use but can be extended for automated reporting or integration with dashboards.
- For custom metrics or additional AI configurations, edit `benchmark.py` or `quick_benchmark.py` accordingly.
- For more details on the AI and game logic, see `README.md` and `ARCHITECTURE.md`.

---

## 🧑‍💻 Example: Saving Results to CSV

Add this to your benchmark script to save results:

```python
import pandas as pd
# ... after collecting results ...
pd.DataFrame([results]).to_csv('benchmark_results.csv', index=False)
```

---

## 📚 References

- [Flask Cores API Documentation](https://pypi.org/project/flask-cores/)
- [Gomoku Project README](./README.md)
