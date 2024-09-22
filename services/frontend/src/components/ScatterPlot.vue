<template>
  <div>
    <div style="height: 80vh; width: 100vh">
      <div id='myScatterPlot' style="height: inherit; width: inherit"></div>
    </div>
  </div>
</template>


<script>
import Plotly from 'plotly.js/dist/plotly';
export default {
  name: "ScatterPlot",
  props: [
    "selectedCategory"
  ],
  data: () => ({
    ScatterPlotData: {x: [], y: [], name: [], cat: []},
    CatColorMap: {
      "tech": "blue",
      "health": "green",
      "bank": "red"
    }
  }),
  mounted() {
    this.fetchData()
  },
  watch: {
    selectedCategory: function () {
      this.ScatterPlotData.x = [];
      this.ScatterPlotData.y = [];
      this.ScatterPlotData.cat = [];
      this.fetchData();
    }
  },
  methods: {
    async fetchData() {
      // req URL to retrieve companies from backend
      var reqUrl = 'http://127.0.0.1:5000/companies?category=' + this.selectedCategory
      // await response and data
      const response = await fetch(reqUrl)
      const responseData = await response.json();
      // transform data to usable by scatterplot
      responseData.forEach((company) => {
        this.ScatterPlotData.name.push(company.name)
        this.ScatterPlotData.x.push(company.founding_year)
        this.ScatterPlotData.y.push(company.employees)
        this.ScatterPlotData.cat.push(company.category)
      })
      // after the data is loaded, draw the plot
      this.drawScatterPlot()
    },
    drawScatterPlot() {

      // get for each point the color from the colormap
      var colors = this.ScatterPlotData.cat.map((cat) => {
        return this.CatColorMap[cat]
      })

      // Also create "invisible traces" for the legend, only show those categories that appear
      var legendTraces = []
      var uniqueCats = [...new Set(this.ScatterPlotData.cat)]
      uniqueCats.forEach((cat) => {
        legendTraces.push({
          x: [null],
          y: [null],
          mode: 'markers',
          type: 'scatter',
          marker: {
            color: this.CatColorMap[cat],
            size: 12
          },
          name: cat,
          showlegend: true
        })
      })

      var trace1 = {
        x: this.ScatterPlotData.x,
        y: this.ScatterPlotData.y,
        text: this.ScatterPlotData.name,
        mode: 'markers',
        type: 'scatter',
        marker: {
          color: colors,
          size: 12
        },
        showlegend: false // we dont want to show that one on the legend
      };
      var data = [trace1].concat(legendTraces);
      var layout = {
        xaxis: {
          title: "Founding Year"
        },
        yaxis: {
          title: "Number of Employees"
        },
        title: {
          text: 'Overview of ' + this.selectedCategory + ' companies',
          font: {
              size: 20
          }
        },
        showlegend: true,
        legend: {x: 0.05, y: 1},
        
      };
      var config = {responsive: true, displayModeBar: false};
      Plotly.newPlot('myScatterPlot', data, layout, config);
      this.clickScatterPlot();
    },
    clickScatterPlot() {
      var that = this
      var myPlot = document.getElementById('myScatterPlot')
      myPlot.on('plotly_click', function (data) {
        for (var i = 0; i < data.points.length; i++) {

          // get the index of point
          let pn = data.points[i].pointNumber;

          // emit event to change the currently selected company in the a) configuration panel
          // and b) update the Profit View
          that.$emit('changeCurrentlySelectedCompany', pn + 1)

          // revert all colors
          var colors = Array(15).fill('#00000');

          // and change currently selected color to blue
          colors[pn] = '#3777ee';

          // update the marker and plot
          var update = {'marker': {color: colors, size: 12}};
          Plotly.restyle('myScatterPlot', update);
        }
      });
    }
  }
}
</script>
