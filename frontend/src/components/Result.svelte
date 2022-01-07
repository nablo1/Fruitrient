<!-- Authors: Idrees, Ruthger -->
<script lang="ts">
  import { createEventDispatcher } from 'svelte'

  const dispatch = createEventDispatcher()
  export let results: any
</script>

<div class="card bg-base-100 lg:h-96 ">
  <div class="card-body overflow-y-auto overflow-x-hidden">
    <button
      on:click={() => dispatch('onClose')}
      class="btn btn-circle btn-sm btn-outline absolute top-3 right-8 z-10"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        class="inline-block w-4 h-4 stroke-current"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M6 18L18 6M6 6l12 12"
        />
      </svg>
    </button>
    <div class="flex flex-row justify-between mb-4">
      <h1 class="card-title text-4xl">Result</h1>
      <div class="w-1/2 mr-10">
        <div class="flex flex-row justify-between items-center">
          <span>Total Correct:</span>
          <span>{results.total_correct}</span>
        </div>
        <div class="flex flex-row justify-between">
          <span>Total Incorrect:</span>
          <span>{results.total_incorrect}</span>
        </div>
      </div>
    </div>
    <table class="table w-full table-compact mb-4">
      <thead>
        <tr>
          <th>#</th>
          <th>Predicted</th>
          <th>Expected</th>
          <th>Is Correct</th>
        </tr>
      </thead>
      <tbody>
        {#each results.results as result, i}
          <tr>
            <th>{i}</th>
            <td
              >{result.result.name} ({result.result.fresh
                ? 'Fresh'
                : 'Rotten'})</td
            >
            <td
              >{result.expected_name} ({result.expected_fresh
                ? 'Fresh'
                : 'Rotten'})</td
            >
            <td>{result.is_correct}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</div>
