import axios from "axios";

const HTTP = axios.create({
  baseURL: "http://127.0.0.1:8000/",
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
          "Content-Type": "application/x-www-form-urlencoded",
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

function createFormBody(credentials: any[]) {
  const formBody: string[] = [];
  for (const property in credentials) {
    const encodedKey = encodeURIComponent(property);
    const encodedValue = encodeURIComponent(credentials[property]);
    formBody.push(encodedKey + "=" + encodedValue);
  }
  return formBody.join("&");
}

const USER_AUTHOR_ID_COOKIE = "InstatonneAuthorId";

export { createHTTP, createFormBody, USER_AUTHOR_ID_COOKIE };
