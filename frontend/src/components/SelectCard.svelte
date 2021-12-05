<script lang="ts">
  export let options: any[] = []
  export let transform = (opt: any) => opt
  export let selected: any = undefined

</script>

<div class="card compact side bg-base-100 h-full">
  <div class="flex-row items-center space-x-4 card-body">
    <p class="card-title">Select Version</p>
    <select class="select select-bordered w-full max-w-xs" bind:value={selected}>
      {#each options as option}
        <option value={option}>{transform(option)}</option>
      {/each}
    </select>
  </div>
</div>
