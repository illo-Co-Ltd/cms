import axios from 'axios'
import router from '../router'

const state = {
  userid: '',
  username: '',
  company: '',
}
const mutations = {
  
}
const actions = {
  // login request
  login({dispatch}, loginObj) {
    axios.post('server/auth/login', loginObj, {withCredentials: true})
      .then(res => {
        if(res.status == 200) {
          // login success
          let access_token = res.data.access_token
          sessionStorage.setItem("access_token", access_token)
        } else if(res.status == 401) {
          alert(res.data.message)
        }
        router.push('/dashboard')
      })
      .catch((e) => {
        console.log("err:",e)
      })
  },
  register({dispatch}, registObj) {
    axios.post('server/data/user', registObj)
      .then((res) => {
        if(!res.data.reason){
          router.push('/login')
        } else {
          console.log("fail:" + res)
        }
      }).catch((e) => {
        console.log("err:",e)
      })
  },
  logout() {
    sessionStorage.removeItem("access_token")
      //location.reload()
      axios.post('server/auth/logout')
      .then((response) => {
        console.log(response);
        router.push('/login')
      }).catch((e) => {
        console.log("err:",e)
      })
  },
  getMemberInfo() {
    let access_token = sessionStorage.getItem("access_token")
    if(access_token != null)
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
    
    axios.get('server/data/user')
      .catch(() => {
        console.log("no User data")
      })
  },
}
export default {state, mutations, actions}