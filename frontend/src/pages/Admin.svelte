<script lang="ts">
  import Chart from '../components/Chart.svelte'
  import FileUpload from '../components/FileUpload.svelte'
  import NavBar from '../components/NavBar.svelte'
  import SelectCard from '../components/selectCard.svelte'
  import SmallCard from '../components/smallCard.svelte'

  const titleOne = 'Latest Version'
  const titleTwo = 'Accuracy'
  const textOne = 'V.5'
  const textTwo = '69,69%'
  const mlVersions = ['v.1', 'v.2', 'v.3', 'v.4', 'v.5']
  const labels = ['v.1', 'v.2', 'v.3', 'v.4', 'v.5']
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
    <SmallCard {titleOne} {textOne} {textTwo} {titleTwo} />
  </div>
  <div class="shadow-lg rounded-box">
    <SmallCard titleOne={'Previous Version'} {textOne} {textTwo} {titleTwo} />
  </div>
  <div class="row-span-3">
    <FileUpload />
  </div>
  <div class="shadow-lg rounded-box">
    <SmallCard
      titleOne={'Currently being used'}
      {textOne}
      {textTwo}
      {titleTwo}
    />
  </div>
  <div class="shadow-lg rounded-box">
    <SelectCard options={mlVersions} />
  </div>
  <div class="card col-span-1 row-span-2 shadow-lg xl:col-span-2 bg-base-100">
    <div class="card-body">
      <h2 class="my-4 text-4xl font-bold card-title">Statistics</h2>
      <Chart {labels} />
    </div>
  </div>
</div>
