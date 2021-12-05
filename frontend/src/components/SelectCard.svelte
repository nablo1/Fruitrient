<script lang="ts">
  export let options: string[] = []
</script>

<div class="card compact side bg-base-100 h-full">
  <div class="flex-row items-center space-x-4 card-body">
    <p class="card-title">Select Version</p>
    <select class="select select-bordered w-full max-w-xs">
      <option>Choose ML Version</option>
      {#each options as option}
        <option>{option}</option>
      {/each}
    </select>
  </div>
</div>
