<template>
  <div>
    <v-container fluid>
      <v-row>
        <v-col cols="12" md="6">
          <v-row>
            <v-col cols="12" sm="12">
              <div class="control-panel-font">Company Overview</div>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="12">
              <v-select
                :items="categories.values"
                label="Select a category"
                dense
                v-model="categories.selectedValue"
                @change="changeCategory">
              </v-select>
            </v-col>
          </v-row>
        </v-col>
        <v-col cols="12" md="6">
          <v-row>
            <v-col cols="12" sm="12">
              <div class="control-panel-font">Company Detail</div>
            </v-col>
            <v-col cols="12" sm="12">
              <v-select
                :items="companies.names"
                label="Select a company"
                dense
                v-model="companies.selectedValue">
            </v-select>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="12">
              <v-select
                :items="algorithm.values"
                label="Select an algorithm"
                dense
                v-model="algorithm.selectedValue"
                @change="changeAlgorithm">
              </v-select>
            </v-col>
          </v-row>
          <v-row v-if="typeof poem === 'string' && poem.length > 0">
            <v-col cols="12" sm="12">
              <div class="control-panel-font"><strong>Poem about the selected company:</strong></div>
              <p>{{ poem }}</p>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="12">
              <v-row>
                <Poem
                  :selectedCompany="companies.values[companies.names.indexOf(companies.selectedValue)]"
                  :selectedCompanyName="companies.selectedValue"
                />
              </v-row>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="6">
          <v-row>
            <ScatterPlot
              :key="scatterPlotId"
              :selectedCategory="categories.selectedValue"
              @changeCurrentlySelectedCompany="changeCurrentlySelectedCompany"
            />
          </v-row>
        </v-col>
        <v-col cols="12" md="6">
          <v-row>
            <LinePlot
              :key="linePlotId"
              :selectedCompany="companies.values[companies.names.indexOf(companies.selectedValue)]"
              :selectedCompanyName="companies.selectedValue"
              :selectedAlgorithm="algorithm.selectedValue"
            />
          </v-row>
          <v-row>
            <PiePlot
              :key="piePlotId"
              :selectedCompany="companies.values[companies.names.indexOf(companies.selectedValue)]"
              :selectedCompanyName="companies.selectedValue"
            />
          </v-row>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>


<style scoped>
.control-panel-font {
  font-family: "Open Sans", verdana, arial, sans-serif;
  align-items: center;
  font-size: 15px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  display: flex;
  font-weight: 500;
  height: 40px;
}
.sideBar {
  border-right: 1px solid rgba(0, 0, 0, 0.1);
  background: #fafafa;
  padding-left: 17px;
  height: calc(100vh - 50px);
}
</style>


<script>
import LinePlot from './LinePlot.vue';
import ScatterPlot from './ScatterPlot.vue';
import PiePlot from './PiePlot.vue';
import Poem from './Poem.vue';


export default {
  name: 'HelloWorld',
  
  // eslint-disable-next-line
  components: {ScatterPlot, LinePlot, PiePlot, Poem},

  data: () => ({
    categories: {
      values: ['All', 'tech', 'health', 'bank'],
      selectedValue: 'All'
    },
    companies: {
      values: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
      names: ["alphabet","apple","amazon","microsoft","meta","united health","johnson and johnson","pfizer","cvs health","mckesson","ubs","credit suisse","jp morgan","goldman sachs","bank of america"],
      selectedValue: "alphabet"
    },
    algorithm: {
      values: ['none', 'random', 'regression'],
      selectedValue: 'none'
    },
    poemCounter: 0,
    scatterPlotId: 0,
    linePlotId: 0,
    piePlotId: 0
  }),

  // mounted() {
  //   this.fetchPoem(this.companies.values[this.companies.names.indexOf(this.companies.selectedValue)]);
  // },

  methods: {
    // async fetchPoem(companyId) {
    //   try {
    //     const response = await axios.get(`http://localhost:5000/llm/groq/poem/${companyId}`);
    //     this.poem = response.data;
    //   } catch (error) {
    //     console.error("Error fetching the poem:", error);
    //   }
    // },
    changeCategory() {
      this.scatterPlotId += 1;
    },
    changeCompany() {
      this.linePlotId += 1;
      this.piePlotId += 1;
      // this.fetchPoem(this.companies.values[this.companies.names.indexOf(this.companies.selectedValue)]);
    },
    changeAlgorithm() {
          this.linePlotId += 1
    },
    changeCurrentlySelectedCompany(companyId) {
      // id to name
      this.companies.selectedValue = this.companies.names[this.companies.values.indexOf(companyId)]
      this.changeCompany()
    }
  },

  watch: {
    'companies.selectedValue': function(newValue, oldValue) {
      this.changeCompany();
    }
  }
}
</script>
