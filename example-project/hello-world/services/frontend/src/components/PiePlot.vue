<template>
  <div>
    <div style="height: 80vh; width: 90vh">
      <div id='myPiePlot' style="height: inherit; width: inherit"></div>
    </div>
  </div>
</template>



<script>
import Plotly from 'plotly.js/dist/plotly';
export default {
  
  name: "PiePlot",
  
  props: ["selectedCompany", "selectedCompanyName"],

  data: () => ({
    PiePlotData: {
      profits: [],
      labels: [],
      pull: [],
      category: ""
    }
  }),
  
  mounted() {
    this.fetchData()
  },

  watch: {
    selectedCompany() {
      this.PiePlotData.profits = [];
      this.PiePlotData.labels = [];
      this.PiePlotData.pull = [];
      this.PiePlotData.category = "";
      this.fetchData();
    }
  },
  
  methods: {
    async fetchData() {

      // req the selected company to find out the category. We dont care about the algorithm
      var reqUrl_single = 'http://127.0.0.1:5000/companies/' + this.selectedCompany + '?algorithm=random';

      // await response and data
      var response_single = await fetch(reqUrl_single)
      var responseData_single = await response_single.json();

      // extract the category
      var selectedCategory = responseData_single.category;
      this.PiePlotData.category = selectedCategory;
      console.log("This is the category for the pie plot: " + selectedCategory);

      // req URL to retrieve all companies of the selected category
      var reqUrl = 'http://127.0.0.1:5000/companies?category=' + selectedCategory;
      // await response and data
      var response = await fetch(reqUrl);
      var responseData = await response.json();
      
      // for each company, summarise the profits
      responseData.forEach((c) => {
        // extract for each company the sum of the profits
        let sum = c.profit.reduce((sum, profit_item) => sum + profit_item.value, 0);
        this.PiePlotData.profits.push(sum);
        this.PiePlotData.labels.push(c.name);
        
        // Set the pull property. Pull puts emphasis on our selected company
        c.id === this.selectedCompany ? this.PiePlotData.pull.push(0.1) : this.PiePlotData.pull.push(0);
      })
      // draw the plot after the data is transformed
      this.drawPiePlot()
    },
    drawPiePlot() {
      var trace = {
        values: this.PiePlotData.profits,
        labels: this.PiePlotData.labels,
        pull: this.PiePlotData.pull,
        // values: [20,20,60],
        // labels: ["a","b","c"],
        type: 'pie',
      };
      
      var layout = {
        title: {
            text: 'Profit distribution of category: ' + this.PiePlotData.category + '<br>Selected company: ' + this.selectedCompanyName,
            font: {
                size: 20
            }
        },
        // title: "Profit distribution of category: " + this.PiePlotData.category + "\nSelected company: " + this.selectedCompanyName,
      };
      var config = {};
      Plotly.newPlot('myPiePlot', [trace], layout, config);
    }
  }
}
</script>