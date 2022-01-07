// Author: Idrees, Ruthger
import axios from 'axios'
import { NutritionFact, RecipesWithIngredient } from './types'

const ApiUrl = 'http://localhost:8000'
const Api = axios.create({
  baseURL: ApiUrl,
})

export interface Classifier {
  id: number
  name: string
  performance: number
  generation: number
  creation_date: string
}

export interface ActiveClassifier {
  id: number
  classifier: Classifier
  selected_date: string
}

export interface NewClassifier {
  name: string
  labels: { [key: string]: number }
  model_bytes: Uint8Array
  image_format: 'L' | 'RGB'
  image_size_y: number
  image_size_x: number
  verify_dataset_id: number
}

export interface Prediction {
  id: number
  name: string
  fresh: boolean
  image?: string
}

export interface PerfCheckData {
  labels: string[],
  data: Uint8Array[]
}

export interface PerfCheckResult {
  results: [{
    result: Prediction,
    is_correct: boolean,
    expected_name: string,
    expected_fresh: boolean
  }],
  total_correct: number,
  total_incorrect: number
}

export const classifiers = async (): Promise<Classifier[]> =>
  (await Api.get('/classifiers')
    .then(({ data }) => data)
    .catch(() => [])) as Classifier[]

export const active_classifier = async (): Promise<ActiveClassifier | null> =>
  (await Api.get('/active_classifiers/-1')
    .then(({ data }) => data)
    .catch(() => null)) as ActiveClassifier

export const active_classifier_history = async (): Promise<
  ActiveClassifier[]
> =>
  (await Api.get('/active_classifiers')
    .then(({ data }) => data)
    .catch(() => [])) as ActiveClassifier[]

export const set_active_classifier = async (
  classifier_id: number
): Promise<Boolean> =>
  await Api.post('/active_classifiers', { id: classifier_id })
    .then(() => true)
    .catch(() => false)

export const classify = async (
  img_data: Uint8Array
): Promise<Prediction | null> =>
  await Api.put('/user/classify', img_data, {
    headers: { 'Content-Type': 'image' },
  })
    .then(({ data }) => data as Prediction)
    .catch(() => null)

export const upload_classifier = async (
  { model_bytes, image_format, image_size_x, image_size_y, name, labels, verify_dataset_id }: NewClassifier
): Promise<Boolean> => {
  const data = new FormData()
  data.append('model_bytes', new Blob([model_bytes.buffer]))
  console.log({ name, image_format, image_size_x, image_size_y })
  data.append('meta', new Blob([JSON.stringify({ name, image_format, image_size_x, image_size_y, verify_dataset_id })], { type: 'application/json' }))
  data.append(
    'labels',
    new Blob([JSON.stringify(labels)], { type: 'application/json' })
  )

  return await Api.post('/classifiers', data)
    .then(() => true)
    .catch(() => false)
}

export const nutrition_facts = async (
  ingredient: string
): Promise<NutritionFact | null> =>
  await Api.get(`/nutrition_facts/${ingredient.replace(' ', '%20')}`)
    .then(({ data }) => data)
    .catch(() => null)

export const recipes_with_ingredient = async (
  ingredient: string
): Promise<RecipesWithIngredient[] | null> =>
  await Api.get(`/recipes/${ingredient.replace(' ', '%20')}`)
    .then(({ data }) => data)
    .catch(() => null)

const prediction_image_url = (id: number) => `${ApiUrl}/predictions/${id}/image`

export const predictions = async (): Promise<Prediction[]> =>
  await Api.get('/predictions')
    .then(({ data }) =>
      data.map((data: Prediction) => {
        return { ...data, image: prediction_image_url(data.id) }
      })
    )
    .catch(() => [])

export const retrain_model = async (model_id: number, dataset_id: number, dataset_verify_id: number): Promise<boolean> =>
  await Api.put(`/admin/retrain/${model_id}`, { dataset_id, dataset_verify_id })
    .then(() => true)
    .catch(() => false)

export const check_perf = async (classifier_id: number, dataset_id: number): Promise<PerfCheckResult | null> =>
  await Api.put(`/admin/check_perf/${classifier_id}`, { dataset_id })
    .then(({ data }) => data)
    .catch(() => null)


export interface DatasetData {
  name: string,
  labels: { name: string, fresh: boolean }[],
  data: Uint8Array[]
}

export const post_dataset = async ({ name, labels, data }: DatasetData): Promise<boolean> => {
  const form = new FormData()
  form.append("name", new Blob([name], { type: 'text/plain' }))
  form.append("labels", new Blob([JSON.stringify(labels)], { type: 'application/json' }))

  console.log(data)
  data.forEach((data, i) => {
    form.append(`image${i}`, new Blob([data.buffer], { type: 'image' }))
  })

  return await Api.post(`/datasets`, form).then(() => true).catch(() => false)
}

export interface Dataset {
  id: number,
  name: string,
  image_count: number
}

export const get_datasets = async (): Promise<Dataset[]> =>
  await Api.get("/datasets").then(({ data }) => data).catch(() => [])

export const delete_dataset = async (id: number): Promise<boolean> => {
  return false
}

export default Api
