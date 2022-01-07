<!-- Authors: Idrees, Ruthger -->
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
        <span>Dataset</span>
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
    <button
      on:click={() =>
        dispatch('submitted', {
          dataset: datasets[selected_dataset],
          model: models[selected_model],
        })}
      class={`btn w-full btn-xs btn-outline ${
        loading && 'loading btn-disabled'
      }`}>Check</button
    >
  </div>
</div>
