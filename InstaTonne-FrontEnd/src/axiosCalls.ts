import axios from 'axios';
import Cookies from 'js-cookie';

// axios.defaults.headers.common['Cookie'] = `csrftoken=${Cookies.get('csrftoken')}`
axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken')

// document.cookie = 'csrftoken=sWfOLaFW6ZWSVLajTUOOP8OL4Y2irJIw'

const HTTP = axios.create({
  baseURL: 'http://localhost:8000/',
  // headers: {
  //   c
  // }
  
  headers: {
    // 'content-Type': 'application/json',
    // "Accept": "/",
    // "Cache-Control": "no-cache",
    // 'Cookie': document.cookie
  },
  withCredentials: true,
})

function createHTTP(url: string) {
  return {
      async post(data: string) {
          return HTTP.post(`${url}`, data).then(response => {
              return response.data
          })
      },
      async get() {
        // console.log(document.cookie)
        return HTTP.get(url)
      },
    //   async patch(element) {
    //       console.log(element)
    //       return HTTP.patch(`${url}${element.id}/`, element).then(response => {
    //           console.log(response)
    //           return response.data
    //       })
    //   },
    //   async delete(id) {
    //       HTTP.delete(`${url}${id}/`)
    //       return id
    //   },
    //   async list(queryParams = '') {
    //       return HTTP.get(`${url}${queryParams}`).then(response => {
    //           return response.data.results
    //       })
    //   }
  }
}

export default createHTTP
