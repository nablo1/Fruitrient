<script>
  import Dropzone from 'svelte-file-dropzone'
  import { createEventDispatcher } from 'svelte'

  export let fileType = '*'
  export let uploadText = 'Drop a file, or click to select a file'
  export let title = 'Upload'

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
          dispatch('fileLoaded', evt.target.result)
        }
      }
    }
  }
</script>

<div class="card compact w-full h-full">
  <div class="flex-col justify-start items-start space-x-4 card-body gap-2">
    <Dropzone
      on:drop={handleFilesSelect}
      minSize={1}
      accept={fileType}
      multiple={false}
      disableDefaultStyles={false}
      containerClasses="w-full rounded-box h-full justify-center"
    >
      <p>{uploadText}</p>
    </Dropzone>
    <div>
      <h2 class="flex card-title">
        {#if progress}
          <p class="btn btn-ghost btn-sm btn-circle loading" />
        {/if}
        {title}
      </h2>
    </div>
  </div>
</div>
