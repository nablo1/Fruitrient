<script lang="ts">
  import InfoCard from '../components/InfoCard.svelte'
  import NavBar from '../components/NavBar.svelte'
  import NutritionCard from '../components/NutritionCard.svelte'
  import RecepiCard from '../components/RecepiCard.svelte'
  import UploadImage from '../components/UploadImage.svelte'
  import WebcamCard from '../components/WebcamCard.svelte'
</script>

<div
  class="grid grid-cols-1 gap-6 p-10 xl:grid-cols-9 lg:bg-base-200 rounded-box"
>
  <div class="col-span-1 xl:col-span-9 shadow-lg">
    <NavBar />
  </div>
  <div
    class="col-span-1 row-span-3 shadow-lg xl:col-span-3 bg-base-100 rounded-box"
  >
    <InfoCard />
  </div>
  <div class="row-span-3 shadow-lg xl:col-span-3 bg-base-100 rounded-box">
    <UploadImage />
  </div>
  <div class="shadow-lg row-span-3 xl:col-span-3 bg-base-100 rounded-box">
    <WebcamCard />
  </div>
  <div class="shadow-lg xl:col-span-2 bg-base-100 rounded-box">
    <RecepiCard />
  </div>
  <div class="shadow-lg xl:col-span-2 bg-base-100  rounded-box">
    <RecepiCard />
  </div>
  <div class="shadow-lg xl:col-span-2 bg-base-100  rounded-box">
    <RecepiCard />
  </div>
  <div class="row-span-3 p-4 shadow-lg xl:col-span-3 bg-base-100  rounded-box">
    <NutritionCard />
  </div>
</div>
