(async function(){
    // 1) fetch your data
    const date = new Date().toISOString().slice(0,10);
    const resp = await fetch(`/api/weights/${date}`);
    const data = await resp.json(); 
    // data: [{ticker, volatility, weight},…]  
  
    // 2) sort descending by weight, take top N
    const N = 50;
    const top = data
      .sort((a,b)=> b.weight - a.weight)
      .slice(0, N);
  
    // 3) build indicators (angles) & series values
    // ECharts radar needs an array of {name, max}
    const indicators = top.map(d=>({
      name: d.ticker,
      max: Math.max(...top.map(x=>x.weight))*1.1
    }));
    // series: a single array of weights
    const values = top.map(d=> d.weight );
    // color map: volatility → hue or lightness
    const colors = top.map(d=> {
      // map volatility [min…max] → hue 0→360
      return `hsl(${ (d.volatility - Math.min(...top.map(x=>x.volatility)))
                      / (Math.max(...top.map(x=>x.volatility)) - Math.min(...top.map(x=>x.volatility))) 
                    * 240 }, 70%, 50%)`;
    });
  
    // 4) configure chart
    const chart = echarts.init(document.getElementById('main'));
    const option = {
      backgroundColor: '#fff',
      title:{ text:`Top ${N} Risk Drivers (${date})`, left:'center' },
      tooltip: {
        formatter: ({ dataIndex }) => {
          const d = top[dataIndex];
          return [
            ` ${d.ticker}`,
            ` Weight: ${(d.weight*100).toFixed(2)}%`,
            ` Vol: ${(d.volatility*100).toFixed(2)}%`
          ].join('<br/>');
        }
      },
      radar: {
        shape: 'circle',
        radius: '75%',
        startAngle: 90,              // start at top
        splitNumber: 5,
        indicator: indicators,
        axisName: { fontSize:12, color:'#333' },
        splitLine: { lineStyle:{ color:'#ddd' } },
        axisLine:  { lineStyle:{ color:'#aaa' } },
        splitArea: { show:false }
      },
      series: [{
        type: 'radar',
        data: [{
          value: values,
          name: 'Weight Spiral',
          itemStyle: { 
            color: (params)=> colors[params.dataIndex],
          },
          lineStyle: { 
            width:1, 
            color: (params)=> colors[params.dataIndex],
            opacity:0.8
          },
          symbol: 'circle',
          symbolSize:4
        }],
        emphasis: {
          lineStyle:{ width:3 },
          itemStyle:{ opacity:1, borderColor:'#000' }
        },
        animationDuration: 1500,
        animationEasing: 'cubicOut'
      }]
    };
    chart.setOption(option);
  })();  