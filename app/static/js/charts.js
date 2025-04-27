// app/static/js/charts.js

async function loadData(date) {
    const [volRes, wRes] = await Promise.all([
      fetch("/api/volatility_30d"), 
      fetch(`/api/weights/${date}`)
    ]);
    return { vol: await volRes.json(), weights: await wRes.json() };
  }
  
  function populateTickerDropdown(vol) {
    const select = document.getElementById("ticker");
    const tickers = [...new Set(vol.map(d => d.ticker))].sort();
    tickers.forEach(t => {
      const opt = document.createElement("option");
      opt.value = opt.textContent = t;
      select.appendChild(opt);
    });
  }
  
  function drawRadial(volData, ticker) {
    const series = volData
      .filter(d => d.ticker === ticker)
      .sort((a, b) => new Date(a.date) - new Date(b.date));
    const T = series.length;
    const angle = d3.scaleLinear().domain([0, T]).range([0, 2 * Math.PI]);
    const rMax = d3.max(series, d => d.volatility);
    const radius = d3.scaleLinear().domain([0, rMax]).range([0, 250]);
    const line = d3.lineRadial()
      .angle((_, i) => angle(i))
      .radius(d => radius(d.volatility))
      .curve(d3.curveCardinalClosed);
  
    const svg = d3.select("#radial").attr("viewBox", [-300, -300, 600, 600]);
    svg.selectAll("*").remove();
    svg.append("path")
      .datum(series)
      .attr("d", line)
      .attr("fill", "steelblue").attr("fill-opacity", 0.3)
      .attr("stroke", "steelblue");
  }
  
  function drawRiskShare(weights) {
    const labels = weights.map(d => d.ticker);
    const data   = weights.map(d => d.weight);
  
    const ctx = document.getElementById("riskChart").getContext("2d");
    if (window.riskChart) window.riskChart.destroy();
    window.riskChart = new Chart(ctx, {
      type: "polarArea",
      data: { labels, datasets: [{ data }] },
      options: {
        plugins: {
          title: { display: true, text: `Risk Shares on ${weights[0].date}` }
        }
      }
    });
  }
  
  (async () => {
    // Use today's date (ISO) or replace with your latest file date
    const date = new Date().toISOString().slice(0, 10);
    const { vol, weights } = await loadData(date);
    populateTickerDropdown(vol);
    drawRadial(vol, vol[0].ticker);
    drawRiskShare(weights);
  
    document.getElementById("ticker").onchange = e =>
      drawRadial(vol, e.target.value);
  })();  