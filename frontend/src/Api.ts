import axios from 'axios'

const Api = axios.create({
  baseURL: process.env.ENDPOINT || 'http://localhost:3100/api',
})

export default Api
