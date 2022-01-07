<!-- Authors: Idrees, Ruthger -->
<script lang="ts">
  import { createEventDispatcher } from 'svelte'
  import { Classifier, Dataset } from '../Api'

  export let models: Classifier[]
  export let datasets: Dataset[]
  export let loading: boolean

  let selected_model: number
  let selected_dataset: number
  let selected_dataset_verify: number

  const setup = (_: any) => {
    selected_model = 0
    selected_dataset = 0
    selected_dataset_verify = 0
  }

  $: {
    setup([models, datasets]) // only trigger when exports change
  }

  const dispatch = createEventDispatcher()
</script>

<div class="card w-full h-full bg-base-100">
  <div class="card-body flex flex-col justify-between w-full">
    <p class="card-title text-center capitalize">Retrain Model</p>
    <div class="form-control w-full mb-2">
      <label class="input-group input-group-xs">
        <span>Model</span>
      <select
        class="select select-bordered select-xs w-full max-w-xs mx-2"
        bind:value={selected_model}
      >
        {#each models as option, i}
          <option value={i}>{option.name} v{option.generation}</option>
        {/each}
      </select>
      </label>
    </div>
    <div class="form-control w-full mb-2">
      <label class="input-group input-group-xs">
        <span>TrainDataset</span>
      <select
        class="select select-bordered select-xs w-full max-w-xs mx-2"
        bind:value={selected_dataset}
      >
        {#each datasets as option, i}
          <option value={i}>{option.name}</option>
        {/each}
      </select>
      </label>
    </div>
    <div class="form-control w-full mb-2">
      <label class="input-group input-group-xs">
        <span>TestDataset</span>
      <select
        class="select select-bordered select-xs w-full max-w-xs mx-2"
        bind:value={selected_dataset_verify}
      >
        {#each datasets as option, i}
          <option value={i}>{option.name}</option>
        {/each}
      </select>
      </label>
    </div>
    <div class="w-full">
      <button
        on:click={() =>
          dispatch('submitted', {
            dataset: datasets[selected_dataset],
            dataset_verify: datasets[selected_dataset_verify],
            model: models[selected_model],
          })}
        class={`btn w-full btn-xs btn-outline ${
          loading && 'loading btn-disabled'
        }`}>Retrain</button
      >
    </div>
  </div>
</div>
