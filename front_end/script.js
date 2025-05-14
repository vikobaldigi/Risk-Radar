// Global variables
let svg, width, height, center, innerRadius, outerRadius;
let currentData = null;
let currentPath = null;

// Initialize the visualization
async function initViz() {
    // SVG setup
    svg = d3.select("#viz");
    width = +svg.attr("width") || svg.node().clientWidth;
    height = +svg.attr("height") || svg.node().clientHeight;
    center = [width/2, height/2];
    innerRadius = width * 0.2;
    outerRadius = width * 0.45;

    // Add glow filter
    const defs = svg.append("defs");
    const glow = defs.append("filter").attr("id", "glow");
    glow.append("feGaussianBlur")
        .attr("stdDeviation", "4")
        .attr("result", "coloredBlur");
    const feMerge = glow.append("feMerge");
    feMerge.append("feMergeNode").attr("in", "coloredBlur");
    feMerge.append("feMergeNode").attr("in", "SourceGraphic");

    // Initialize color scale
    initColorScale();

    // Load initial data
    await updateViz();
}

// Initialize color scale
function initColorScale() {
    const colorScale = d3.scaleSequential()
        .domain([0, 1])
        .interpolator(d3.interpolateViridis);

    const scaleWidth = 200;
    const scaleHeight = 20;
    const scaleSvg = d3.select("#color-scale")
        .append("svg")
        .attr("width", scaleWidth)
        .attr("height", scaleHeight);

    const gradient = scaleSvg.append("defs")
        .append("linearGradient")
        .attr("id", "color-gradient")
        .attr("x1", "0%")
        .attr("x2", "100%")
        .attr("y1", "0%")
        .attr("y2", "0%");

    gradient.selectAll("stop")
        .data(d3.range(0, 1.1, 0.1))
        .enter()
        .append("stop")
        .attr("offset", d => `${d * 100}%`)
        .attr("stop-color", d => colorScale(d));

    scaleSvg.append("rect")
        .attr("width", scaleWidth)
        .attr("height", scaleHeight)
        .style("fill", "url(#color-gradient)");
}

// Update visualization with new data
async function updateViz() {
    const date = document.getElementById("date-select").value;
    const resp = await fetch(`/api/weights/${date}`);
    const data = await resp.json();
    currentData = data;

    const vols = data.map(d => d.volatility);
    const N = vols.length;
    const maxVol = d3.max(vols);

    // Scale volatility to radial displacement
    const volScale = d3.scaleLinear()
        .domain([0, maxVol])
        .range([0, outerRadius - innerRadius]);

    // Color scale for volatility
    const colorScale = d3.scaleSequential()
        .domain([0, maxVol])
        .interpolator(d3.interpolateViridis);

    // Generate points
    const theta = d3.scaleLinear().domain([0, N]).range([0, 2*Math.PI]);
    const noise = d3.randomNormal.source(d3.randomLcg(42))(0, 1);

    const points = d3.range(N).map(i => {
        const angle = theta(i);
        const rBase = innerRadius + volScale(vols[i]);
        const offset = noise() * 5;
        const r = rBase + offset;
        return {
            x: center[0] + r * Math.cos(angle),
            y: center[1] + r * Math.sin(angle),
            volatility: vols[i]
        };
    });

    // Create or update path
    const line = d3.line()
        .x(d => d.x)
        .y(d => d.y)
        .curve(d3.curveCardinalClosed.tension(0.5));

    if (currentPath) {
        currentPath.transition()
            .duration(750)
            .attr("d", line(points));
    } else {
        currentPath = svg.append("path")
            .attr("d", line(points))
            .attr("fill", "none")
            .attr("stroke", "#39ff14")
            .attr("stroke-width", 2)
            .attr("filter", "url(#glow)");
    }

    // Add interactive points
    const pointsGroup = svg.selectAll(".point")
        .data(points);

    pointsGroup.exit().remove();

    const pointsEnter = pointsGroup.enter()
        .append("circle")
        .attr("class", "point")
        .attr("r", 4)
        .attr("fill", d => colorScale(d.volatility))
        .style("opacity", 0.7)
        .on("mouseover", showTooltip)
        .on("mouseout", hideTooltip);

    pointsGroup.merge(pointsEnter)
        .transition()
        .duration(750)
        .attr("cx", d => d.x)
        .attr("cy", d => d.y)
        .attr("fill", d => colorScale(d.volatility));
}

// Tooltip functions
function showTooltip(event, d) {
    const tooltip = d3.select("#tooltip");
    tooltip.transition()
        .duration(200)
        .style("opacity", 1);
    
    tooltip.html(`Volatility: ${d.volatility.toFixed(4)}`)
        .style("left", (event.pageX + 10) + "px")
        .style("top", (event.pageY - 28) + "px");
}

function hideTooltip() {
    d3.select("#tooltip")
        .transition()
        .duration(500)
        .style("opacity", 0);
}

// Event listeners
document.getElementById("update-btn").addEventListener("click", updateViz);

// Initialize visualization
initViz();  