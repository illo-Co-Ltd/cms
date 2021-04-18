import axios from 'axios'

const state = {
  src: "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7",
}

const actions = {
  loadImage({dispatch}){
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
  } 
}

export default {
  state,
  actions
}