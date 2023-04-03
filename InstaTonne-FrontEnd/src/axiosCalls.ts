import axios from "axios";

const backend_url = "https://cmput404-group6-instatonne.herokuapp.com";

// try{
//   if(import.meta.env.DEV){
//     backend_url = import.meta.env.VITE_BACKEND_URL;
//   }
//   else if(import.meta.env.PROD){
//     backend_url = import.meta.env.VITE_BACKEND_URL_PROD;
//   }

// }
// catch (e) {
//   backend_url = "https://cmput404-group6-instatonne.herokuapp.com//";//'http://127.0.0.1:8000/';
// }

const HTTP = axios.create({
  baseURL: backend_url,
  withCredentials: true,
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFToken",
});

function createHTTP(url: string) {
  return {
    async post(data: string) {
      console.log(data, 444);
      return HTTP.post(`${url}`, data, {
        headers: {
          "Content-Type": "application/json",
        },
      }).then((response) => {
        return response.data;
      });
    },
    async get() {
      return HTTP.get(url);
    },
    async put(data: string) {
      return HTTP.put(`${url}`, data, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      }).then((response) => {
        return response.data;
      });
    },
    async delete() {
      return HTTP.delete(url);
    },
    //   async list(queryParams = '') {
    //       return HTTP.get(`${url}${queryParams}`).then(response => {
    //           return response.data.results
    //       })
    //   }
  };
}

// create http request to retrieve csrf token
createHTTP("csrf/").get();

function createFormBody(credentials: any[]) {
  const formBody: string[] = [];
  for (const property in credentials) {
    const encodedKey = encodeURIComponent(property);
    const encodedValue = encodeURIComponent(credentials[property]);
    formBody.push(encodedKey + "=" + encodedValue);
  }
  return formBody.join("&");
}

export { createHTTP, createFormBody };
