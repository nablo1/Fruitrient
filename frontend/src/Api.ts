import axios from 'axios'

const Api = axios.create({
  baseURL: 'http://localhost:8000',
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
  name: string,
  type: number,
  fresh: number,
}

export interface NewClassifier {
  name: string,
  labels: { [key: number]: string },
  model_bytes: Uint8Array
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

export const upload_classifier =
  async (classifier: NewClassifier): Promise<Boolean> => {
    const data = new FormData()
    data.append("model_bytes", new Blob([classifier.model_bytes.buffer]))
    data.append("name", new Blob([classifier.name], { type: 'text/plain'}))
    data.append("labels", new Blob([JSON.stringify(classifier.labels)], { type: 'application/json'}))

    return await Api.post('/classifiers', data).then(() => true).catch(() => false)
  }

export default Api
