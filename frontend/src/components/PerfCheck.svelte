<script lang="ts">
  import { createEventDispatcher } from 'svelte'
  import { Classifier, Dataset } from '../Api'

  export let models: Classifier[]
  export let datasets: Dataset[]
  export let loading: boolean

  let selected_model: number
  let selected_dataset: number

  const setup = () => {
    selected_model = 0
    selected_dataset = 0
  }

  $: [models, datasets], setup()

  const dispatch = createEventDispatcher()
</script>

<div class="card w-full h-full bg-base-100">
  <div class="card-body flex flex-col justify-between">
    <p class="card-title text-center capitalize">Performance Check</p>
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
      <p class="card-title mb-0">Dataset</p>
      <select
        class="select select-bordered w-full max-w-xs"
        bind:value={selected_dataset}
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
          model: models[selected_model],
        })}
      class={`btn btn-block btn-square btn-outline ${
        loading && 'loading btn-disabled'
      }`}>Check</button
    >
  </div>
</div>
