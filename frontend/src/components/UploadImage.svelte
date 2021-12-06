<script>
  import Dropzone from 'svelte-file-dropzone'
  import { createEventDispatcher } from 'svelte'

  const dispatch = createEventDispatcher()
  let progress = false

  const handleFilesSelect = (e) => {
    const { acceptedFiles } = e.detail
    const reader = new FileReader()
    if (acceptedFiles.length) {
      reader.readAsArrayBuffer(acceptedFiles[0])
      reader.onload = () => (progress = true)
      reader.onloadend = (evt) => {
        progress = false
        if (evt.target.readyState === FileReader.DONE) {
          dispatch('imageLoaded', evt.target.result)
        }
      }
    }
  }
</script>

// if we end up doing some custom stuff wiht file upload we can use this to just
upload image

<div class="card compact w-full h-full">
  <div class="flex-col justify-start items-start space-x-4 card-body gap-2">
    <Dropzone
      on:drop={handleFilesSelect}
      minSize={1}
      accept="image/*"
      multiple={false}
      disableDefaultStyles={false}
      containerClasses="w-full rounded-box h-full justify-center"
    >
      <p>Drap an Image, or click to select an image</p>
    </Dropzone>
    <div>
      <h2 class="flex card-title">
        {#if progress}
          <p class="btn btn-ghost btn-sm btn-circle loading" />
        {/if}
        Upload Image
      </h2>
      <!-- <h2 class="card-title ">Upload Image</h2> -->
      <!-- <p class="text-base-content text-opacity-40">Loading</p> -->
    </div>
  </div>
</div>
