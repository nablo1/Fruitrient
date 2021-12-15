<script lang="ts">
  import { createEventDispatcher } from 'svelte'

  export let accurcy: string
  export let modelId: string
  export let loading: boolean
  export let retrainModelResponse: any = null

  const dispatch = createEventDispatcher()

  let response: object | null
</script>

<div class="card w-full h-full bg-base-100">
  <div class="card-body flex flex-col justify-between">
    <p class="card-title text-center capitalize">Retrain current model</p>
    <div class="flex flex-row justify-between">
      <p class="card-title mb-0">Model Id</p>
      <p>{modelId}</p>
    </div>
    <div class="flex flex-row justify-between mb-2">
      <p class="card-title mb-0">
        {#if retrainModelResponse}
          <span>New&nbsp</span>
        {/if}
        Accurcy
      </p>
      <p>{accurcy}</p>
    </div>
    {#if retrainModelResponse}
      <div class="flex flex-row justify-evenly">
        <button
          class="btn btn-outline px-7"
          on:click={() => dispatch('onKeep', modelId)}>Keep</button
        >
        <button
          class="btn btn-outline"
          on:click={() => dispatch('onDismiss', modelId)}>Dismiss</button
        >
      </div>
    {:else}
      <button
        on:click={() => dispatch('retrain', modelId)}
        class={`btn btn-block btn-square btn-outline ${
          loading && 'loading btn-disabled'
        }`}>Retrain</button
      >
    {/if}
  </div>
</div>
