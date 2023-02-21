import axios from 'axios'

const HTTP = axios.create({
  baseURL: 'http://localhost:8000/service/',
})

function createHTTP(url: string) {
  return {
    //   async post(config) {
    //       return HTTP.post(`${url}`, config).then(response => {
    //           console.log(response)
    //           return response.data
    //       })
    //   },
      async get() {
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
