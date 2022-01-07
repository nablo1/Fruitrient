<script lang="ts">
  import Chart from '../components/Chart.svelte'
  import NavBar from '../components/NavBar.svelte'
  import SelectCard from '../components/SelectCard.svelte'
  import SmallCard from '../components/SmallCard.svelte'

  import {
    ActiveClassifier,
    active_classifier,
    active_classifier_history,
    check_perf,
    Classifier,
    classifiers,
    NewClassifier,
    set_active_classifier,
    retrain_model,
    upload_classifier,
    post_dataset,
    get_datasets,
    Dataset,
  } from '../Api'
  import { onMount } from 'svelte'
  import FileUploadWithForm from '../components/FileUploadWithForm.svelte'
  import Result from '../components/Result.svelte'
  import ModelUpload from '../components/ModelUpload.svelte'
  import PerfCheck from '../components/PerfCheck.svelte'
  import Retrain from '../components/Retrain.svelte'

  const titleOne = 'Currently being used'
  const titleTwo = 'Accuracy'

  let mlVersions = [] as Classifier[]
  let activeMlHistory = [] as ActiveClassifier[]
  let datasets = [] as Dataset[]
  let activeMl = null as ActiveClassifier | null
  let results = null as any

  let waiting_for_train = false
  let train_results: boolean | null = null

  let waiting_for_performance = false

  let testing: any = undefined

  const update_stuff = async (testing: any) => {
    console.log('update stuff', testing, activeMl)
    if (testing && testing.id !== activeMl?.classifier.id) {
      await set_active_classifier(testing.id)
      await update()
    }
  }

  const update = async () => {
    const activeMlHistory_tmp = await active_classifier_history()
    const mlVersions_tmp = await classifiers()
    const datasets_tmp = await get_datasets()
    const activeMl_tmp = await active_classifier()

    activeMlHistory = activeMlHistory_tmp
    mlVersions = mlVersions_tmp
    datasets = datasets_tmp
    activeMl = activeMl_tmp
    testing = mlVersions.find((v) => v.id == activeMl!.classifier.id)!
  }

  $: update_stuff(testing)
  $: console.log('activeMl: ', activeMl)
  $: console.log('mlVersions: ', mlVersions)
  $: console.log('activeMlHistory: ', activeMlHistory)
  $: console.log('datasets: ', datasets)

  onMount(async () => {
    await update()
  })

  const fileLoaded = async (data: CustomEvent) => {
    console.log('data.detail', data.detail)
    const res = await upload_classifier(data.detail as NewClassifier)
    console.log('new model upload res: ', res)
    update()
  }

  const retrainModel = async ({ detail }: CustomEvent) => {
    waiting_for_train = true
    console.log('retraining!')
    train_results = await retrain_model(
      detail.model.id,
      detail.dataset.id,
      detail.dataset_verify.id
    )
    console.log('done!')
    waiting_for_train = false
    update()
  }

  const handlePerfCheck = async (data: CustomEvent) => {
    waiting_for_performance = true
    results = await check_perf(data.detail.model.id, data.detail.dataset.id)
    waiting_for_performance = false
    console.log('perfech res', results)
    update()
  }

  const handleDataSetUpload = async (data: CustomEvent) => {
    console.log(data)
    const res = await post_dataset(data.detail)
    console.log('did we succeed in uploading the dataset? ', res)
    update()
  }
</script>

<div
  class="grid grid-cols-1 gap-6 lg:p-10 lg:pb-20 xl:grid-cols-3 lg:bg-base-200 h-full"
>
  <div
    class="col-span-1 shadow-lg xl:col-span-3 bg-neutral-focus text-neutral-content rounded-box"
  >
    <NavBar />
  </div>
  <div class="shadow-lg rounded-box">
    <SmallCard
      {titleOne}
      textOne={activeMl
        ? `${activeMl.classifier.name} v${activeMl.classifier.generation}`
        : '???'}
      textTwo={activeMl ? activeMl.classifier.performance + '%' : '???'}
      {titleTwo}
    />
  </div>
  <div class="shadow-lg rounded-box">
    <SmallCard
      titleOne={'Previous Version'}
      textOne={activeMlHistory.length > 1
        ? `${activeMlHistory[1]?.classifier.name} v${activeMlHistory[1]?.classifier.generation}`
        : '???'}
      textTwo={activeMlHistory.length > 1
        ? activeMlHistory[1]?.classifier.performance + '%'
        : '???'}
      {titleTwo}
    />
  </div>
  <div class="row-span-2 shadow-lg bg-base-100 rounded-box">
    {#if train_results == null}
      <div class="row-span-2 shadow-lg bg-base-100 rounded-box">
        <Retrain
          {datasets}
          models={mlVersions}
          on:submitted={retrainModel}
          loading={waiting_for_train}
        />
      </div>
    {:else}
      <div class="card w-full h-full bg-base-100">
        <div class="card-body flex flex-col justify-between">
          <p class="card-title text-center capitalize">
            {train_results
              ? 'Succesfully retrained'
              : 'Training did not improve model'}
          </p>
          <button
            on:click={() => (train_results = null)}
            class={`btn btn-block btn-square btn-outline`}>dismiss</button
          >
        </div>
      </div>
    {/if}
  </div>
  <div class="shadow-lg rounded-box">
    <SmallCard
      titleOne={'Latest Version'}
      textOne={mlVersions.length > 0
        ? `${mlVersions[0]?.name} v${mlVersions[0]?.generation}`
        : '???'}
      textTwo={mlVersions.length > 0 ? mlVersions[0]?.performance + '%' : '???'}
      {titleTwo}
    />
  </div>
  <div class="shadow-lg rounded-box">
    <SelectCard
      bind:selected={testing}
      bind:options={mlVersions}
      transform={(el) => `${el.name} v${el.generation}`}
    />
  </div>
  <div class="row-span-2 shadow-lg bg-base-100 rounded-box">
    {#if !results}
      <PerfCheck
        {datasets}
        models={mlVersions}
        on:submitted={handlePerfCheck}
        loading={waiting_for_performance}
      />
    {:else}
      <Result {results} on:onClose={() => (results = null)} />
    {/if}
  </div>
  <div class="card col-span-1 row-span-2 shadow-lg xl:col-span-2 bg-base-100">
    <div class="card-body">
      <h2 class="my-4 text-4xl font-bold card-title">Statistics</h2>
      <Chart
        labels={mlVersions.map((el) => `${el.name} v${el.generation}`)}
        data={mlVersions.map((el) => el.performance)}
      />
    </div>
  </div>
  <div class="row-span-2 shadow-lg bg-base-100 rounded-box">
    <ModelUpload on:fileLoaded={fileLoaded} />
  </div>

  <div class="col-span-1 row-span-1 shadow-lg xl:col-span-2 rounded-box">
    <FileUploadWithForm {mlVersions} on:fileUpload={handleDataSetUpload} />
  </div>
</div>
