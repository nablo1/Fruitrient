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
  <div class="card-body flex flex-col justify-between">
    <p class="card-title text-center capitalize">Retrain Model</p>
    <div class="flex flex-row justify-between">
      <p class="card-title mb-0">Model</p>
      <select
        class="select select-bordered w-full max-w-xs"
        bind:value={selected_model}
      >
        {#each models as option, i}
          <option value={i}>{option.name} v{option.generation}</option>
        {/each}
      </select>
    </div>
    <div class="flex flex-row justify-between">
      <p class="card-title mb-0">Train Dataset</p>
      <select
        class="select select-bordered w-full max-w-xs"
        bind:value={selected_dataset}
      >
        {#each datasets as option, i}
          <option value={i}>{option.name}</option>
        {/each}
      </select>
    </div>
    <div class="flex flex-row justify-between">
      <p class="card-title mb-0">Test Dataset</p>
      <select
        class="select select-bordered w-full max-w-xs"
        bind:value={selected_dataset_verify}
      >
        {#each datasets as option, i}
          <option value={i}>{option.name}</option>
        {/each}
      </select>
    </div>
    <button
      on:click={() =>
        dispatch('submitted', {
          dataset: datasets[selected_dataset],
          dataset_verify: datasets[selected_dataset_verify],
          model: models[selected_model],
        })}
      class={`btn btn-block btn-square btn-outline ${
        loading && 'loading btn-disabled'
      }`}>Retrain</button
    >
  </div>
</div>
