<template>
  <div>
    <div style="height: 80vh; width: 100vh">
      <div id='myLinePlot' style="height: inherit; width: inherit"></div>
    </div>
  </div>
</template>



<script>
import Plotly from 'plotly.js/dist/plotly';
export default {
  
  name: "LinePlot",
  
  props: ["selectedCompany", "selectedCompanyName", "selectedAlgorithm"],

  data: () => ({
    LinePlotData: { 
      "solid" : {x: [], y: []},
      "prediction" : {x: [], y: []}
    }
  }),
  
  mounted() {
    this.fetchData()
  },

  watch: {
    selectedCompany() {
      this.LinePlotData.solid.x = [];
      this.LinePlotData.solid.y = [];
      this.LinePlotData.prediction.x = [];
      this.LinePlotData.prediction.y = [];
      this.fetchData();
    },
    selectedAlgorithm() {
      this.LinePlotData.solid.x = [];
      this.LinePlotData.solid.y = [];
      this.LinePlotData.prediction.x = [];
      this.LinePlotData.prediction.y = [];
      this.fetchData();
    }
  },
  
  methods: {
    async fetchData() {
      // req URL to retrieve single company from backend
      var reqUrl = 'http://127.0.0.1:5000/companies/' + this.selectedCompany + '?algorithm=' + this.selectedAlgorithm
      // await response and data
      const response = await fetch(reqUrl)
      const responseData = await response.json();
      // transform data to usable by lineplot
      responseData.profit.forEach((profit) => {
        if (profit.year >= 2021) {
          this.LinePlotData.prediction.x.push(profit.year)
          this.LinePlotData.prediction.y.push(profit.value)
        }
        if (profit.year <= 2021) {
          this.LinePlotData.solid.x.push(profit.year)
          this.LinePlotData.solid.y.push(profit.value)
        }
      })
      // draw the lineplot after the data is transformed
      this.drawLinePlot()
    },
    drawLinePlot() {
      var trace_solid = {
        x: this.LinePlotData.solid.x,
        y: this.LinePlotData.solid.y,
        type: 'scatter',
        mode: 'lines+markers',
        name: "History",
        marker: {
          color: 'blue'
        },
        line: {
          color: 'blue'
        }
      };
      var trace_prediction = {
        x: this.LinePlotData.prediction.x,
        y: this.LinePlotData.prediction.y,
        type: 'scatter',
        mode: 'lines+markers',
        name: "Prediction (if algorithm is selected)",
        marker: {
          color: 'orange'
        },
        line: {
          color: 'orange',
          dash: 'dot'
        }
      };
      
      // We exclude prediciton trace if there is only one value (2021)
      var data = this.LinePlotData.prediction.x.length > 1 ? [trace_prediction, trace_solid] : [trace_solid];
      var layout = {
        xaxis: {
          title: "Year",
          tickformat: "d",
          autotick: false
        },
        yaxis: {
          title: "Profit"
        },
        showlegend: true,
        legend: {x: 0.05, y: 1},
        title: {
          text: 'Profit View of selected company ' + this.selectedCompanyName,
          font: {
              size: 20
          }
        }
      };
      var config = {responsive: true, displayModeBar: false}
      Plotly.newPlot('myLinePlot', data, layout, config);
    }
  }
}
</script>