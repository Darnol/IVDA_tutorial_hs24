<template>
    <div style="width: 90%">
        <v-row align="left" justify="left" class="mt-1 mb-0">
            <h3>A poem about selected company "{{ $props.selectedCompanyName }}" using attribute "<span style="color: red;">{{ $props.selectedCompanyName }}</span>":</h3>
        </v-row>
        <v-row class="mt-1 mb-5">
          <em v-html="poem"></em>
        </v-row>
    </div>
</template>


<script>
import axios from 'axios';
export default {
  
  name: "PoemComponent",
  
  props: ["selectedCompany", "selectedCompanyName"],

  data: () => ({
    poem: ""
  }),
  
  mounted() {
    this.fetchPoem()
  },

  watch: {
    selectedCompany() {
      this.fetchPoem();
    }
  },
  
  methods: {
    async fetchPoem() {
      try {
        const response = await axios.get(`http://localhost:5000/llm/groq/poem/${this.selectedCompany}`);
        this.poem = response.data;
        // highlight the information used
        this.poem = this.poem.replace(new RegExp(this.selectedCompanyName, 'gi'), (match) => `<span style="color: red;">${match}</span>`);
      } catch (error) {
        console.error("Error fetching the poem:", error);
      }
    }
  }
}
</script>