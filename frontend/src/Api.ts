import axios from 'axios'

const Api = axios.create({
  baseURL: process.env.ENDPOINT || 'http://localhost:8000',
})

export interface Classifier {
  id: number,
  name: string,
  performance: number,
  creation_date: string
}

export interface ActiveClassifier {
  id: number,
  classifier: Classifier,
  selected_date: string
}

export interface Classification {
  fruit: {
    name: string,
    type: number,
    certainty: number
  },
  quality: {
    quality: number,
    certainty: number
  }
}

export const classifiers =
  async (): Promise<Classifier[]> =>
    await Api.get('/classifiers').then(({data}) => data).catch(() => []) as Classifier[]

export const active_classifier =
  async (): Promise<ActiveClassifier | null> =>
    await Api.get('/active_classifiers/-1').then(({data}) => data).catch(() => null) as ActiveClassifier

export const active_classifier_history =
  async (): Promise<ActiveClassifier[]> =>
    await Api.get('/active_classifiers').then(({data}) => data).catch(() => []) as ActiveClassifier[]

export const set_active_classifier =
  async (classifier_id: number): Promise<Boolean> =>
    await Api.post('/active_classifiers', {id: classifier_id}).then(() => true).catch(() => false)

export const classify =
  async (img_data: Uint8Array): Promise<Classification | null> =>
    await Api.put('/user/classify', img_data, { headers: { 'Content-Type': 'image' } }).then(({data}) => data as Classification).catch(() => null)

export default Api
