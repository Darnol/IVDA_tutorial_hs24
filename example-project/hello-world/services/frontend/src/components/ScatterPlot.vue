<template>
  <div>
    <v-row align="center" justify="center" class="mt-1 mb-0">
      <h3>Overview of {{ $props.selectedCategory }} Companies</h3>
    </v-row>
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
    ScatterPlotData: {x: [], y: [], name: [], cat: []}
  }),
  mounted() {
    this.fetchData()
  },
  watch: {
    selectedCategory: function () {
      this.ScatterPlotData.x = [];
      this.ScatterPlotData.y = [];
      this.ScatterPlotData.name = [];
      this.ScatterPlotData.cat = [];
      this.fetchData();
    }
  },
  methods: {
    async fetchData() {
      // req URL to retrieve companies from backend
      var reqUrl = 'http://127.0.0.1:5000/companies?category=' + this.selectedCategory
      console.log("ReqURL " + reqUrl)
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

      // color cycle for the categories
      const color_cycle = [
        "green",
        "blue",
        "red",
        "yellow",
        "orange",
        "purple",
        "brown",
        "pink",
        "cyan",
        "magenta",
        "grey",
        "lightblue"
      ]
      // Gather all unique categories present in the data
      let unique_cat = [];
      unique_cat.push(...new Set(this.ScatterPlotData.cat));
      // boolean if only one unique category is present (then we dont show colors, but black)
      let single_cat = unique_cat.length === 1;
      // map the categories to colors
      let cat_color_map = {};
      unique_cat.forEach((cat, index) => {
        single_cat ? cat_color_map[cat] = 'black' : cat_color_map[cat] = color_cycle[index]
      })
      

      // I want to show a legend, so i have to separate the data points into cateogories
      let traces = [];

      // Create a trace for each unique category
      unique_cat.forEach((cat, ) => {
        // For cat, collect all indizes belonging to that cat
        let category_indices = this.ScatterPlotData.cat
          .map((c, i) => (c === cat ? i : null))
          .filter(i => i !== null);
        
        // Filter data for the current category
        let trace_x = category_indices.map(i => this.ScatterPlotData.x[i]);
        let trace_y = category_indices.map(i => this.ScatterPlotData.y[i]);
        let trace_text = category_indices.map(i => this.ScatterPlotData.name[i]);

        // get the color of that cat
        let cat_color = cat_color_map[cat];

        // Create a trace for this category
        traces.push({
          x: trace_x,
          y: trace_y,
          text: trace_text,
          mode: 'markers',
          type: 'scatter',
          name: cat, // This will be shown in the legend
          marker: {
            color: cat_color,
            size: 12
          }
        });
      });

      var layout = {
        xaxis: {
          title: "Founding Year"
        },
        yaxis: {
          title: "Number of Employees"
        },
        showlegend: true, // Show the legend
        legend: {
          title: {
            text: 'Categories'
          },
          x: 1,
          xanchor: 'right',
          y: 1
        }
      };
      var config = {responsive: true, displayModeBar: false};
      Plotly.newPlot('myScatterPlot', traces, layout, config);
      this.clickScatterPlot();
    },
    clickScatterPlot() {
      var that = this
      var myPlot = document.getElementById('myScatterPlot')
      myPlot.on('plotly_click', function (data) {
        for (var i = 0; i < data.points.length; i++) {

          console.log("clickScatterPlot: This is the data:");
          console.log(data);

          // get the index of point
          let pn = data.points[i].pointNumber;

          // emit event to change the currently selected company in the a) configuration panel
          // and b) update the Profit View
          that.$emit('changeCurrentlySelectedCompany', pn + 1)

          // revert all colors
          var colors = ['#00000' * 15]

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
