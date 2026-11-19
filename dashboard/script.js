let chart;
let labels = [];
let dataPoints = [];
let colors = [];
let rssiValues = [];
let started = false;
let interval = null;

// 🔊 Alert sound
function playAlert() {
    const audio = new Audio("https://www.soundjay.com/buttons/beep-01a.mp3");
    audio.play().catch(() => {});
}

async function sendDataAuto() {

    const isAnomaly = Math.random() > 0.8;

    const packet = isAnomaly
        ? 300 + Math.random()*50
        : 100 + Math.random()*20;

    const rssi = isAnomaly
        ? -90 + Math.random()*10
        : -60 + Math.random()*5;

    // Show values
    document.getElementById("packet").innerText = packet.toFixed(0);
    document.getElementById("rssi").innerText = rssi.toFixed(0);

    const response = await fetch(
        `http://127.0.0.1:8000/predict?packet_size=${packet}&rssi=${rssi}`,
        { method: "POST" }
    );

    const result = await response.json();

    const statusDiv = document.getElementById("status");

    if (result.status.includes("ANOMALY")) {
        statusDiv.innerText = "🚨 INTRUSION DETECTED";
        statusDiv.className = "alert";
        colors.push("red");
        playAlert();
    } else {
        statusDiv.innerText = "✅ SYSTEM NORMAL";
        statusDiv.className = "normal";
        colors.push("lime");
    }

    // Accuracy
    document.getElementById("accuracy").innerText =
        (result.accuracy * 100).toFixed(2) + "%";

    labels.push(labels.length);
    dataPoints.push(packet);
    rssiValues.push(rssi);

    if (labels.length > 20) {
        labels.shift();
        dataPoints.shift();
        colors.shift();
        rssiValues.shift();
    }

    if (chart) chart.destroy();

    const ctx = document.getElementById("chart");

    chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Network Activity",
                data: dataPoints,
                borderColor: "#38bdf8",
                tension: 0.4,
                pointBackgroundColor: colors,
                pointRadius: 6
            }]
        },
        options: {
            plugins: {
                legend: { labels: { color: "white" } },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const i = context.dataIndex;
                            return [
                                "📦 Packet: " + dataPoints[i].toFixed(2),
                                "📶 RSSI: " + rssiValues[i].toFixed(0) + " dBm"
                            ];
                        }
                    }
                }
            },
            scales: {
                x: { ticks: { color: "white" } },
                y: { ticks: { color: "white" } }
            }
        }
    });
}

// ▶ Start
function startSystem() {
    if (!started) {
        started = true;
        interval = setInterval(sendDataAuto, 2000);
    }
}

// ⏹ Stop
function stopSystem() {
    started = false;
    clearInterval(interval);

    document.getElementById("status").innerText = "⏹ SYSTEM STOPPED";
    document.getElementById("status").className = "";
}