<script>
  import Dropzone from 'svelte-file-dropzone'
  import { createEventDispatcher } from 'svelte'

  let progress = false
  let accFiles = []
  let rejFiles = []
  let filesByteArray
  const labels = {}
  let name

  const dispatch = createEventDispatcher()
  const handleFilesSelect = (e) => {
    const { acceptedFiles, fileRejections } = e.detail
    accFiles = acceptedFiles
    rejFiles = fileRejections
    acceptedFiles.forEach((e, i) => {
      labels[i] = ''
    })
    console.log('accFiles', { rejFiles, rejFiles })
    const reader = new FileReader()
    if (acceptedFiles.length) {
      reader.readAsArrayBuffer(acceptedFiles[0])
      reader.onload = () => (progress = true)
      reader.onloadend = (evt) => {
        if (evt.target.readyState === FileReader.DONE) {
          filesByteArray = new Uint8Array(evt.target.result)
          progress = false
        }
      }
    }
  }

  const handleSubmit = () => {
    dispatch('fileUpload', { name, labels, model_bytes: filesByteArray })
  }
</script>

<div class="card bg-base-100 lg:h-96">
  <div class="card-body flex lg:flex-row lg:gap-x-10 gap-y-5 overflow-y-auto">
    <div class="lg:h-80 w-full lg:w-1/2">
      <Dropzone
        on:drop={handleFilesSelect}
        minSize={1}
        accept="image/png"
        multiple={false}
        disableDefaultStyles={false}
        containerClasses="w-full rounded-box h-full justify-center"
      >
        <p>Upload as many files as you wish</p>
      </Dropzone>
    </div>

    <div
      class={`flex-grow flex-col flex  ${
        rejFiles.length || !accFiles.length ? 'items-center justify-center' : ''
      }`}
    >
      {#if !rejFiles.length && accFiles.length}
        <form on:submit|preventDefault={handleSubmit} class="overflow-y-auto">
          <p class="text-xl mb-2">Name</p>
          <div class="form-control mb-2">
            <label for="dataLabel" class="input-group input-group-xs">
              <span>ML</span>
              <input
                required
                id="dataName"
                type="text"
                placeholder="Name"
                class="input input-bordered input-xs w-full ml-2 mr-5"
                bind:value={name}
              />
            </label>
          </div>
          <p class="text-xl mb-2">Labels</p>
          {#each accFiles as file, i}
            <div class="form-control mb-2">
              <label for="dataLabel" class="input-group input-group-xs">
                <span>{i}</span>
                <input
                  required
                  id={'dataLabel' + i}
                  type="text"
                  placeholder="Label"
                  class="input input-bordered input-xs w-full mx-5"
                  bind:value={labels[i]}
                />
              </label>
            </div>
          {/each}
          <div class="form-control mb-2  mr-5">
            <button
              class={`btn btn-xs btn-outline btn-block ${
                progress && 'loading'
              }`}
              type="submit">submit</button
            >
          </div>
        </form>
      {:else if rejFiles.length}
        <p>Please Upload correct file format</p>
      {:else}
        <p>Please Upload Data to start traing new ML model</p>
      {/if}
    </div>
  </div>
</div>
