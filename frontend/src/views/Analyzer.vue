<template>
<div v-if="hasImage">
  <base-header type="gradient-success" class="pb-2 pb-8 pt-5 pt-md-2">
    <div class="a-main">
      <div>
        <card class="mb-2">
          <template slot="header">
            <h2>Image : {{this.mainImage}}</h2>
          </template>
          <template>
            <img class="img-fluid"
                :src="require(`../assets${mainImage}`)" />
          </template>
        </card>
      </div>
    </div>
  </base-header>
  <div class="container-fluid mt--7">
    <div class="row">
      <div class="col-xl-8 mb-5 mb-xl-0">
        <card type="default" header-classes="bg-transparent">
            <div slot="header" class="row align-items-center">
                <div class="col">
                    <h6 class="text-light text-uppercase ls-1 mb-1">Overview</h6>
                    <h5 class="h3 text-white mb-0">Cell Culture</h5>
                </div>
                <div class="col">
                    <ul class="nav nav-pills justify-content-end">
                        <li class="nav-item mr-2 mr-md-0">
                            <a class="nav-link py-2 px-3"
                               href="#"
                               :class="{active: bigLineChart.activeIndex === 0}"
                               @click.prevent="initBigChart(0)">
                                <span class="d-none d-md-block">Month</span>
                                <span class="d-md-none">M</span>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link py-2 px-3"
                               href="#"
                               :class="{active: bigLineChart.activeIndex === 1}"
                               @click.prevent="initBigChart(1)">
                                <span class="d-none d-md-block">Week</span>
                                <span class="d-md-none">W</span>
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
            <line-chart
                    :height="350"
                    ref="bigChart"
                    :chart-data="bigLineChart.chartData"
                    :extra-options="bigLineChart.extraOptions"></line-chart>
        </card>
      </div>
      <div class="col-xl-4">
        <card header-classes="bg-transparent">
            <div slot="header" class="row align-items-center">
                <div class="col">
                    <h6 class="text-uppercase text-muted ls-1 mb-1">Performance</h6>
                    <h5 class="h3 mb-0">Total Count</h5>
                </div>
            </div>

            <bar-chart
                    :height="350"
                    ref="barChart"
                    :chart-data="redBarChart.chartData"
            >
            </bar-chart>
        </card>
      </div>
    </div>
  </div>

<<<<<<< HEAD
  <modal :show.sync="modals.capture"
         size="sm">
    <card type="secondary"
          header-classes="bg-transparent pb-5"
          body-classes="px-lg-5 py-lg-5"
          class="border-0 mb-0">
      <template>
        <div>
          <div class="text-muted text-left mt-2 mb-3">
            <h3>Capture Image</h3>
          </div>
          <div role="form">
            <div class="text-center text-muted mb-4">
              <small>Setting properties of Image</small>
            </div>
            <base-input v-model="captureModal.project"
                        class="mb-3"
                        placeholder="Project Name">
            </base-input>
            <base-input v-model="captureModal.target"
                        placeholder="Target Name">
            </base-input>
            <base-input v-model="captureModal.device"
                        placeholder="Device">
            </base-input>
            <base-input v-model="captureModal.label"
                        placeholder="Description">
            </base-input>
            <base-button type="primary" @click="imageCapture">Create</base-button>
            <base-button type="link" @click="modals.capture=false">close</base-button>
          </div>
        </div>
      </template>
    </card>
  </modal>

=======
>>>>>>> dcd97c19c7fcf18e23ab6b0200281ac49c35bec8
</div>
</template>
<script>
// Charts
import * as chartConfigs from '@/components/Charts/config';
import LineChart from '@/components/Charts/LineChart';
import BarChart from '@/components/Charts/BarChart';

export default {
  components: {
    LineChart,
    BarChart,
  },
  data() {
    return {
      bigLineChart: {
        allData: [
          [0, 20, 10, 30, 15, 40, 20, 60, 60],
          [0, 20, 5, 25, 10, 30, 15, 40, 40]
        ],
        activeIndex: 0,
        chartData: {
          datasets: [],
          labels: [],
        },
        extraOptions: chartConfigs.blueChartOptions,
      },
      redBarChart: {
        chartData: {
          labels: ['2h', '4h', '6h', '8h', '10h', '12h'],
          datasets: [{
            label: 'Sales',
            data: [25, 20, 30, 22, 17, 29]
          }]
        }
      }
    };
  },
  props: {
    mainImage: String,
  }, 
  methods: {
    initBigChart(index) {
      let chartData = {
        datasets: [{
            label: 'Performance',
            data: this.bigLineChart.allData[index]
        }],
        labels: ['0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h'],
      };
      this.bigLineChart.chartData = chartData;
      this.bigLineChart.activeIndex = index;
    },
    imageCapture() {
      axios.post('server/api/camera/capture', this.captureModal)
      .then((response) => {
        this.$parent.updateImage();
        console.log(response);
      }).catch((e) => {
        console.log("err:",e)
      })
      this.modals.capture = false;
    },
  },
  mounted() {
    this.initBigChart(0);
  },
  computed: {
    hasImage() {
      return this.mainImage;
    },
  },
}
</script>
<style scoped>
.a-main {
  padding-top: 24px;
  padding-left: 39px !important;
  padding-right: 39px !important;
}
</style>