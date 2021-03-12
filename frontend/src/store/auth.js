import axios from 'axios'
import router from '../router'

const state = {
  isLogin: false,
}
const mutations = {
  loginSuccess() {
    
  }
}
const actions = {
  // login request
  login({dispatch}, loginObj) {
    axios
      .post('server/auth/login', loginObj, {withCredentials: true})
      .then(res => {
        if(res.status == 200) {
          // login success
          let access_token = res.data.access_token
          sessionStorage.setItem("access_token", access_token)
        } else {
          alert(res.data.message)
        }
        dispatch()
      })
      .catch(() => {
        console.log("?")
        router.push('/dashboard')
      })
  },
  logout() {
    sessionStorage.removeItem("access_token")
      //location.reload()
      axios.post('server/auth/logout')
      .then((response) => {
        console.log(response);
        this.login=false
        router.push('/login')
      }).catch((e) => {
        console.log("err:",e)
      })
  },
  getMemberInfo() {
    let access_token = sessionStorage.getItem("access_token")
    if(access_token != null)
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
    
    axios
      .get('server/auth/whoami')
      .then(res => {
        //alert("로그인상태입니다")
        console.log(res)
      })
      .catch(() => {
        console.log("no User data")
      })
  },
}
export default {state, mutations, actions}