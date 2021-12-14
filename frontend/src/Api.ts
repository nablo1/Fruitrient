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
  creation_date: string
}

export interface ActiveClassifier {
  id: number
  classifier: Classifier
  selected_date: string
}

export interface NewClassifier {
  name: string
  labels: { [key: number]: string }
  model_bytes: Uint8Array
}

export interface Prediction {
  id: number
  name: string
  type: number
  fresh: boolean
  image?: string
}


export interface PerfCheckData {
  labels: number[],
  data: Uint8Array[]
}

export interface PerfCheckResult {
  results: [{
    result: Prediction,
    is_correct: boolean,
    expected: number
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
  classifier: NewClassifier
): Promise<Boolean> => {
  const data = new FormData()
  data.append('model_bytes', new Blob([classifier.model_bytes.buffer]))
  data.append('name', new Blob([classifier.name], { type: 'text/plain' }))
  data.append(
    'labels',
    new Blob([JSON.stringify(classifier.labels)], { type: 'application/json' })
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

export const tryRetrainModel = async (modelId: string): Promise<any> =>
  await Api.post('/retrain', { modelId })
    .then(({ data }) => data)
    .catch(() => null)

export const check_perf = async (classifier_id: number, { labels, data }: PerfCheckData): Promise<PerfCheckResult | null> => {
  if (labels.length != data.length) {
    console.log("THIS DOESNT WORK")
    return null
  }

  const form = new FormData()
  form.append("labels", new Blob([JSON.stringify(labels)], { type: 'application/json' }))

  data.forEach((data, i) => {
    form.append(`image${i}`, new Blob([data.buffer], { type: 'image' }))
  })

  return await Api.put(`/admin/check_perf/${classifier_id}`, form).then(({ data }) => data).catch(() => null)
}

export default Api
