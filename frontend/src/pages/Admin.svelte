<script lang="ts">
  import Chart from '../components/Chart.svelte'
  import FileUpload from '../components/FileUpload.svelte'
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
    set_active_classifier,
    tryRetrainModel,
  } from '../Api'
  import { onMount } from 'svelte'
  import RetrainModel from '../components/RetrainModel.svelte'
  import FileUploadWithForm from '../components/FileUploadWithForm.svelte'

  const titleOne = 'Currently being used'
  const titleTwo = 'Accuracy'

  let mlVersions = [] as Classifier[]
  let activeMlHistory = [] as ActiveClassifier[]
  let activeMl = null as ActiveClassifier | null
  let loading = false
  let currModelId = ''
  let currModelAccurcy = ''
  let retrainModelResponse = true

  let testing: any = undefined

  const update_stuff = async (testing: any) => {
    console.log('update stuff')
    if (
      testing && testing.id !== activeMl?.id
        ? await set_active_classifier(testing.id)
        : false
    ) {
      activeMl = await active_classifier()
      activeMlHistory = await active_classifier_history()
    }
  }

  $: update_stuff(testing)
  $: console.log('activeMl: ', activeMl)
  $: console.log('mlVersions: ', mlVersions)
  $: console.log('activeMlHistory: ', activeMlHistory)

  onMount(async () => {
    mlVersions = await classifiers()
    activeMl = await active_classifier()
    activeMlHistory = await active_classifier_history()

    testing = activeMl
    currModelId = activeMl ? activeMl.classifier.name : ''
    currModelAccurcy = activeMl ? activeMl.classifier.performance + '%' : ''
  })

  const fileLoaded = async (data: CustomEvent) => {
    console.log(data.detail)
  }

  const retrainModel = async () => {
    loading = true
    retrainModelResponse = await tryRetrainModel(currModelId)
    loading = false
  }

  const handleDismiss = (data: CustomEvent) => {
    console.log(data.detail)
  }

  const handleOnKeep = (data: CustomEvent) => {
    console.log(data.detail)
  }

  const handleFileUpload = async (data: CustomEvent) => {
    console.log(data.detail)
    console.log(await check_perf(activeMlHistory[0].classifier.id, data.detail))
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
      textOne={activeMl ? activeMl.classifier.name : '???'}
      textTwo={activeMl ? activeMl.classifier.performance + '%' : '???'}
      {titleTwo}
    />
  </div>
  <div class="shadow-lg rounded-box">
    <SmallCard
      titleOne={'Previous Version'}
      textOne={activeMlHistory.length > 1
        ? activeMlHistory[1]?.classifier.name
        : '???'}
      textTwo={activeMlHistory.length > 1
        ? activeMlHistory[1]?.classifier.performance + '%'
        : '???'}
      {titleTwo}
    />
  </div>
  <div class="row-span-2 shadow-lg bg-base-100 rounded-box">
    <RetrainModel
      {loading}
      {retrainModelResponse}
      modelId={currModelId}
      accurcy={currModelAccurcy}
      on:retrain={retrainModel}
      on:onDismiss={handleDismiss}
      on:onKeep={handleOnKeep}
    />
  </div>
  <div class="shadow-lg rounded-box">
    <SmallCard
      titleOne={'Latest Version'}
      textOne={mlVersions.length > 0 ? mlVersions[0]?.name : '???'}
      textTwo={mlVersions.length > 0 ? mlVersions[0]?.performance + '%' : '???'}
      {titleTwo}
    />
  </div>
  <div class="shadow-lg rounded-box">
    <SelectCard
      bind:selected={testing}
      options={mlVersions}
      transform={(el) => el.id + ' - ' + el.name}
    />
  </div>
  <div class="card col-span-1 row-span-2 shadow-lg xl:col-span-2 bg-base-100">
    <div class="card-body">
      <h2 class="my-4 text-4xl font-bold card-title">Statistics</h2>
      <Chart
        labels={mlVersions.map((el) => el.name)}
        data={mlVersions.map((el) => el.performance)}
      />
    </div>
  </div>
  <div class="row-span-2 shadow-lg bg-base-100 rounded-box">
    <FileUpload
      on:fileLoaded={fileLoaded}
      fileType="*"
      title="Upload a file"
      uploadText="Drop a file, or click to select a file"
    />
  </div>
  <div class="col-span-1 row-span-1 shadow-lg xl:col-span-2 rounded-box">
    <FileUploadWithForm on:fileUpload={handleFileUpload} />
  </div>
</div>
