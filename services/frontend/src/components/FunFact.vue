<template>
    <div style="width: 90%">
        <v-row align="left" justify="left" class="mt-1 mb-0">
            <h3>
              A fun fact about selected company "{{ $props.selectedCompanyName }}" using attribute
              "<span style="color: red;">{{ $props.selectedCompanyName }}</span>",
              "<span style="color: red;">{{ category }}</span>" and
              "<span style="color: red;">{{ founding_year }}</span>":</h3>
        </v-row>
        <v-row class="mt-1 mb-5">
            <em>{{ funfact }}</em>
        </v-row>
    </div>
</template>


<script>
import axios from 'axios';
export default {
  
  name: "FunFactComponent",
  
  props: ["selectedCompany", "selectedCompanyName"],

  data: () => ({
    funfact: "",
    category: "",
    founding_year: ""
  }),
  
  mounted() {
    this.fetchFunFact()
  },

  watch: {
    selectedCompany() {
      this.fetchFunFact();
    }
  },
  
  methods: {
    async fetchFunFact() {
      try {
        const response = await axios.get(`http://localhost:5000/llm/groq/funfact/${this.selectedCompany}`);
        console.log(response.data);
        this.funfact = response.data.funfact;
        this.category = response.data.category;
        this.founding_year = response.data.founding_year;
      } catch (error) {
        console.error("Error fetching the funfact:", error);
      }
    }
  }
}
</script>