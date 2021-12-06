<script lang="ts">
  // components
  import FileUpload from '../components/FileUpload.svelte'
  import InfoCard from '../components/InfoCard.svelte'
  import NavBar from '../components/NavBar.svelte'
  import NutritionCard from '../components/NutritionCard.svelte'
  import RecepiCard from '../components/RecepiCard.svelte'
  import WebcamCard from '../components/WebcamCard.svelte'

  // import Api from '../Api'

  const imageLoaded = async (data: CustomEvent) => {
    // const post = await Api.post('/image', data.detail).catch(e=>console.log(e))
    console.log(data.detail)
  }
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
    <FileUpload
      on:fileLoaded={imageLoaded}
      title="Upload an Image"
      fileType="image/*"
      uploadText="Drop an Image, or click to select an image"
    />
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
