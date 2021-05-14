<template>
  <div>
    <div class="d-container">
      <img class="img-fluid img-mt" :src="src" alt="">
      <!-- <button class="testtest" @click="loadImage">refresh Image</button> -->
    </div>
    <div class="d-o bg-white d-o-shadow"
          v-bind:style="{top:this.$store.state.dimens.header+'px',
                         width:this.$store.state.dimens.optional+'px'}">
      <div class="d-o-margin">
        <h4>color</h4>
        <base-input>
          <select class="form-control" v-model="color">
            <option>RGB</option>
            <option>Grayscale</option>
          </select>
        </base-input>
        <div><base-button class="float-right" @click="colorApply">apply</base-button></div>
        <div class="d-o-content-m-t d-o-divider"></div>

        <h4>blur</h4>
        <base-input>
          <select class="form-control" v-model="blur.selected">
            <option>average</option>
            <option>median</option>
            <option>gaussian</option>
          </select>
        </base-input>
        <h5>kernel size</h5>
        <base-slider v-model="blur.ksize" :range="{min: 1, max: 11}">{{blurSnap}}</base-slider>
        <h6>{{this.blur.ksize}}</h6>
        <div><base-button class="float-right" @click="blurApply">apply</base-button></div>
        <div class="d-o-content-m-t d-o-divider"></div>

        <h4>Normalize</h4>
        <base-input>
          <select class="form-control" v-model="normalize.selected">
            <option>global</option>
            <option>clahe</option>
          </select>
        </base-input>
        <h5>clip limit</h5>
        <base-slider v-model="normalize.clipLimit" :range="{min: 1, max: 10}"></base-slider>
        <h6>{{this.normalize.clipLimit}}</h6>
        <h5>tile Grid Size</h5>
        <base-slider v-model="normalize.tileGridSize" :range="{min: 1, max: 50}">{{normalizeSnap}}</base-slider>
        <h6>{{this.normalize.tileGridSize}}</h6>
        <div><base-button class="float-right" @click="normalizeApply">apply</base-button></div>
        <div class="d-o-content-m-t d-o-divider"></div>

        <h4>Threshold</h4>
        <base-input>
          <select class="form-control" v-model="threshold.selected">
            <option>global</option>
            <option>adaptive</option>
          </select>
        </base-input>
        <h5>mode</h5>
        <div v-if="threshold.selected=='global'">
          <base-input>
            <select class="form-control" v-model="threshold.mode">
              <option>simple</option>
              <option>otsu</option>
            </select>
          </base-input>
        </div>
        <div v-if="threshold.selected=='adaptive'">
          <base-input>
            <select class="form-control" v-model="threshold.mode">
              <option>mean</option>
              <option>gaussian</option>
            </select>
          </base-input>
        </div>
        <h5>type</h5>
        <base-input>
          <select class="form-control" v-model="threshold.type">
            <option>THRESH_BINARY</option>
            <option>THRESH_BINARY_INV</option>
            <option>THRESH_TRUNC</option>
            <option>THRESH_TOZERO</option>
            <option>THRESH_TOZERO_INV</option>
          </select>
        </base-input>
        <h5>max value</h5>
        <base-slider v-model="threshold.maxval" :range="{min: 0, max: 255}">{{thresholdSnap}}</base-slider>
        <h6>{{this.threshold.maxval}}</h6>
        <div v-if="threshold.selected=='global'">
          <h5 >threash</h5>
          <base-slider v-model="threshold.threash" :range="{min: 0, max: 255}">{{thresholdSnap}}</base-slider>
          <h6>{{this.threshold.threash}}</h6>
        </div>
        <div v-if="threshold.selected=='adaptive'">
          <h5>bsize</h5>
          <base-slider v-model="threshold.bsize" :range="{min: 1, max: 50}">{{thresholdSnap}}</base-slider>
          <h6>{{this.threshold.bsize}}</h6>
          <h5>c</h5>
          <base-slider v-model="threshold.c" :range="{min: 0, max: 50}"></base-slider>
          <h6>{{this.threshold.c}}</h6>
        </div>
        <div><base-button class="float-right" @click="thresholdApply">apply</base-button></div>
        <div class="d-o-content-m-t d-o-divider"></div>
      </div>
    </div>
  </div>
</template>

<script>
import BaseButton from '../components/BaseButton.vue'
import BaseDropdown from '../components/BaseDropdown.vue'
import BaseSlider from '../components/BaseSlider.vue'
import axios from 'axios'

export default {
  components: { BaseDropdown, BaseButton, BaseSlider },
  created() {
    this.getImage()
  },
  data() {
    return{
      color: 'RGB',
      blur: {
        selected: 'average',
        ksize: 7,
      },
      normalize: {
        selected: 'global',
        clipLimit: 5,
        tileGridSize: 25,
      },
      threshold: {
        selected: 'global',
        mode: '',
        type: 'THRESH_BINARY',
        maxval: 0,
        threash: 0,
        bsize: 1,
        c: 0,
      },
      src: "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7",
      taskId: '',
    }
  },
  computed: {
    blurSnap() {
      if(Math.floor(this.blur.ksize)%2 == 0)
        this.blur.ksize = Math.floor(this.blur.ksize) - 1
      else this.blur.ksize = Math.floor(this.blur.ksize)
    },
    normalizeSnap() {
      this.normalize.tileGridSize = Math.floor(this.normalize.tileGridSize)
    },
    thresholdSnap() {
      this.threshold.maxval = Math.floor(this.threshold.maxval)
      this.threshold.threash = Math.floor(this.threshold.threash)
      if(Math.floor(this.threshold.bsize)%2 == 0)
        this.threshold.bsize = Math.floor(this.threshold.bsize) - 1
      else this.threshold.bsize = Math.floor(this.threshold.bsize)
      this.threshold.c = Math.floor(this.threshold.c)
    }
  },
  methods: {
    getImage() {
      let config = {
        url: 'http://localhost:5000/data/image/sample01.png',
        method: 'GET',
        responseType: 'arraybuffer'
      }
      axios(config)
      .then((res) => {
        var bytes = new Uint8Array(res.data);
        var binary = bytes.reduce((data, b) => data += String.fromCharCode(b), '');
        this.src = "data:image/jpeg;base64," + btoa(binary);
      })
    },
    loadImage() {
      let config = {
        url: 'http://localhost:5000/cv/result/' + this.taskId,
        method: 'GET',
        responseType: 'arraybuffer'
      }
      axios(config)
      .then((res) => {
        var bytes = new Uint8Array(res.data);
        var binary = bytes.reduce((data, b) => data += String.fromCharCode(b), '');
        this.src = "data:image/jpeg;base64," + btoa(binary);
      })
    },
    colorApply() {
      if(this.color == 'Grayscale') this.color = 'gray'
      
      axios.post('server/cv/color', {
                                      "path":"sample01.png",
                                    	"params":{
		                                    "cmap": this.color,
	                                    }
                                    })
      .then((res) => {
        this.taskId = res.data
        setTimeout(() => this.loadImage(), 500)
      })

    },
    blurApply() {
      axios.post('server/cv/blur', {
	                                    "path":"sample01.png",
	                                    "params":{
		                                    "method": this.blur.selected,
		                                    "ksize": this.blur.ksize
	                                    }
                                    })
      .then((res) => {
        this.taskId = res.data
        setTimeout(() => this.loadImage(), 500)
      })
    },
    normalizeApply() {
      alert(this.normalize.clipLimit + "|" +typeof(this.normalize.clipLimit))
      const clipLimit = parseFloat(this.normalize.clipLimit)
      axios.post('server/cv/normalize', {
                                      "path":"sample01.png",
                                      "params":{
                                        "method":this.normalize.selected,
                                        "clipLimit": clipLimit,
                                        "tileGridSize":this.normalize.tileGridSize
                                      }
                                    })
      .then((res) => {
        this.taskId = res.data
        setTimeout(() => this.loadImage(), 500)
      })
    },
    thresholdApply() {
      if(this.threshold.selected=='global') {
        alert("추가예정")
      } else {
        axios.post('server/cv/threshold', {
                                        "path":"sample01.png",
                                        "params":{
                                          "method":this.threshold.selected,
                                          "mode":this.threshold.mode,
                                          "thresh_type":this.threshold.type,
                                          "maxval":this.threshold.maxval,
                                          "bsize":this.threshold.bsize,
                                          "c":this.threshold.c
                                        }
                                      })
        .then((res) => {
          this.taskId = res.data
          setTimeout(() => this.loadImage(), 500)
        })
      }
    }
  },
}
</script>

<style scoped>
.d-container{
  margin-left: 250px;
  margin-right: 300px;
}
.d-o{
  position: fixed;
  right: 0;
  bottom: 0;
  overflow: auto;
  background-color: rgb(255, 255, 255);
}
.d-o-shadow{
  box-shadow: -1px 0px 5px rgb(223, 223, 223);
}
.d-o-margin{
  margin: 1.5rem 1rem;
}
.d-o-divider{
  height: 1px;
  background-color: rgb(240, 240, 240);
}
.d-o-content-m-t{
  margin-top: 4.5rem;
  margin-bottom: .5rem;
}
.d-o-scroll{
  overflow: scroll;
}
.img-mt{
  margin-top: 80px;
}
.testtest{
  margin-top: 150px;
  margin-left: 300px;
}
</style>