// benchmark_dashboard.js
// Real-time Gomoku AI Benchmark Dashboard logic

const runBtn = document.getElementById('runBtn');
const algorithmSel = document.getElementById('algorithm');
const boardSizeSel = document.getElementById('boardSize');
const difficultySel = document.getElementById('difficulty');
const trialsInput = document.getElementById('trials');
const logDiv = document.getElementById('log');
const chartCanvas = document.getElementById('benchmarkChart');

let chart;

function log(msg) {
    logDiv.textContent += msg + '\n';
    logDiv.scrollTop = logDiv.scrollHeight;
}

function clearLog() {
    logDiv.textContent = '';
}

function showChart(data) {
    if (chart) chart.destroy();
    chart = new Chart(chartCanvas, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: 'Avg Time per Move (s)',
                    data: data.avgTimes,
                    backgroundColor: '#1976d2',
                },
                {
                    label: 'Avg Nodes per Move',
                    data: data.avgNodes,
                    backgroundColor: '#43a047',
                    yAxisID: 'y1',
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: { display: true, text: 'Seconds' }
                },
                y1: {
                    beginAtZero: true,
                    position: 'right',
                    grid: { drawOnChartArea: false },
                    title: { display: true, text: 'Nodes' }
                }
            }
        }
    });
}

async function runBenchmark() {
    runBtn.disabled = true;
    clearLog();
    log('Starting benchmark...');
    const config = {
        algorithm: algorithmSel.value,
        boardSize: parseInt(boardSizeSel.value),
        difficulty: parseInt(difficultySel.value),
        trials: parseInt(trialsInput.value)
    };
    log(`Config: ${JSON.stringify(config)}`);

    // Call backend API to run benchmark (assume /api/benchmark exists)
    try {
        const resp = await fetch('/api/benchmark', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(config)
        });
        if (!resp.ok) throw new Error('Benchmark failed');
        const result = await resp.json();
        log('Benchmark complete!');
        log(JSON.stringify(result, null, 2));
        // Prepare chart data
        showChart({
            labels: [config.algorithm],
            avgTimes: [result.avg_time_per_move],
            avgNodes: [result.avg_nodes_per_move || 0]
        });
    } catch (e) {
        log('Error: ' + e.message);
    }
    runBtn.disabled = false;
}

runBtn.addEventListener('click', runBenchmark);
