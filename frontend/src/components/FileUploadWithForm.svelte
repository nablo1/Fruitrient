<!-- Authors: Idrees, Ruthger -->
<script lang="ts">
  import Dropzone from 'svelte-file-dropzone'
  import { createEventDispatcher } from 'svelte'
  import { Classifier } from '../Api'

  let progress = false
  let accFiles: any[] = []
  let rejFiles: any[] = []
  let filesByteArray: Promise<Uint8Array>[][] = []
  let labels: string[] = []
  let name: string = ''
  export let mlVersions: Classifier[]
  let selected: any

  const dispatch = createEventDispatcher()
  const handleFilesSelect = (e: any) => {
    const { acceptedFiles, fileRejections } = e.detail
    accFiles = [...accFiles, ...acceptedFiles]
    rejFiles = [...rejFiles, ...fileRejections]
    labels = [...labels, '']
    console.log('accFiles', { accFiles, rejFiles })

    filesByteArray = [
      ...filesByteArray,
      acceptedFiles.map(
        (fil: any) =>
          new Promise((resolve, reject) => {
            const reader = new FileReader()
            reader.readAsArrayBuffer(fil)
            reader.onerror = () => reject()
            reader.onloadend = (evt: any) => {
              if (evt.target.readyState === FileReader.DONE) {
                progress = false
                resolve(new Uint8Array(evt.target.result))
              }
            }
          })
      ),
    ]
  }

  const handleSubmit = async () => {
    let acc: Uint8Array[] = []
    const lbls: string[] = []
    let i = 0
    for (const file of filesByteArray) {
      const bytes = await Promise.all(file)
      bytes.forEach(() => lbls.push(labels[i]))
      acc = [...acc, ...bytes]
      i += 1
    }

    dispatch('fileUpload', {
      labels: lbls,
      data: acc,
      name: selected,
    })
  }
</script>

<div class="card bg-base-100 lg:h-96">
  <div class="card-body flex lg:flex-row lg:gap-x-10 gap-y-5 overflow-y-auto">
    <div class="lg:h-80 w-full lg:w-1/2">
      <Dropzone
        on:drop={handleFilesSelect}
        minSize={1}
        accept="image/*"
        multiple={true}
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
        <form
          autocomplete="off"
          on:submit|preventDefault={handleSubmit}
          class="overflow-y-auto"
        >
          <p class="text-xl mb-2">Name</p>
          <div class="form-control mb-2">
            <label for="dataLabel" class="input-group input-group-xs">
              <span>set</span>
              <input
                type="text"
                bind:value={selected}
                class="input input-bordered input-xs w-full"
              />
            </label>
          </div>
          <p class="text-xl mb-2">Labels</p>
          {#each labels as file, i}
            <div class="form-control mb-2">
              <label for="dataLabel" class="input-group input-group-xs">
                <span>{filesByteArray[i].length}</span>
                <input
                  required
                  id={'dataLabel' + i}
                  type="text"
                  placeholder="Label"
                  class="input input-bordered input-xs w-full"
                  bind:value={labels[i]}
                />
              </label>
            </div>
          {/each}
          <div class="form-control mb-2 mr-5">
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
        <p class="text-xl text-center">
          Please Upload Data to Test The Accuracy of The Model
        </p>
      {/if}
    </div>
  </div>
</div>
