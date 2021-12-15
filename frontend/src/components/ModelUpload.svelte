<script>
  import Dropzone from 'svelte-file-dropzone'
  import { createEventDispatcher } from 'svelte'

  const title = 'Upload'
  let performance = 0
  let name = null
  let model_bytes = null
  let labels = null
  let progress = false
  let accpetedFileLength = 0
  let acceptedFile = false
  let acceptedJson = false

  const dispatch = createEventDispatcher()

  const handleFilesSelect = (e) => {
    const { acceptedFiles, fileRejections } = e.detail
    if (fileRejections.length) return console.log('not correct file')
    accpetedFileLength += acceptedFiles.length
    const reader = new FileReader()
    if (acceptedFiles.length) {
      reader.readAsArrayBuffer(acceptedFiles[0])
      reader.onload = () => (progress = true)
      reader.onloadend = (evt) => {
        progress = false
        if (evt.target.readyState === FileReader.DONE) {
          acceptedFile = true
          model_bytes = new Uint8Array(evt.target.result)
        }
      }
    }
  }

  const handleJsonUpload = (e) => {
    const { acceptedFiles, fileRejections } = e.detail
    if (fileRejections.length) return console.log('not correct file')
    accpetedFileLength += acceptedFiles.length
    const reader = new FileReader()
    if (acceptedFiles.length) {
      reader.readAsText(acceptedFiles[0])
      reader.onload = () => (progress = true)
      reader.onloadend = (evt) => {
        progress = false
        if (evt.target.readyState === FileReader.DONE) {
          acceptedJson = true
          labels = JSON.parse(event.target.result)
        }
      }
    }
  }

  const handleSubmit = () => {
    if (accpetedFileLength == 2)
      dispatch('fileLoaded', { model_bytes, performance, name, labels })
    console.log('Please Upload The Model Firest')
  }
</script>

<div class="card compact w-full h-full">
  <div class="flex-col justify-start items-start space-x-4 card-body gap-2">
    <div class="flex flex-row h-full w-full">
      <Dropzone
        on:drop={handleFilesSelect}
        minSize={1}
        multiple={false}
        disableDefaultStyles={false}
        containerClasses="w-full rounded-box h-full justify-center text-center grow"
      >
        {#if acceptedFile}
          <p>Upload Done</p>
        {:else}
          <p>Drop a file, or click to select a file</p>
        {/if}
      </Dropzone>
      <Dropzone
        on:drop={handleJsonUpload}
        minSize={1}
        accept="application/json"
        multiple={false}
        disableDefaultStyles={false}
        containerClasses="w-full rounded-box h-full justify-center text-center grow"
      >
        {#if acceptedJson}
          <p>Upload Done</p>
        {:else}
          <p>Drop The Model Labels Json, or click to select a Json File</p>
        {/if}
      </Dropzone>
    </div>
    <div class="w-full">
      <h2 class="flex card-title mb-10">
        {#if progress}
          <p class="btn btn-ghost btn-sm btn-circle loading" />
        {/if}
        {title}
      </h2>

      <form on:submit|preventDefault={handleSubmit} class="w-full mt-5">
        <div class="form-control">
          <label class="input-group input-group-xs mb-2">
            <span>Name</span>
            <input
              placeholder="Model Name"
              class="input input-bordered input-xs mx-5 w-full"
              type="text"
              required
              bind:value={name}
            />
          </label>
        </div>
        <div class="form-control">
          <label class="input-group input-group-xs mb-2">
            <span>Performance</span>
            <input
              placeholder="Performance"
              class="input input-bordered input-xs mx-5 w-full"
              type="number"
              required
              bind:value={performance}
            />
          </label>
        </div>
        <button type="submit" class="btn btn-outline w-[96%] btn-xs"
          >Submit</button
        >
      </form>
    </div>
  </div>
</div>
