<script lang="ts">
  export let titleOne: string
  export let titleTwo: string
  export let textOne: string
  export let textTwo: string
</script>

<div class="card compact side bg-base-100 h-full">
  <div class=" card-body">
    <div class="flex justify-between align-middle items-center">
      <h2 class="card-title">{titleOne}</h2>
      <p class="text-base-content text-opacity-60">{textOne}</p>
    </div>
    <div class="flex justify-between align-middle items-center ml-0 mx-0">
      <h2 class="card-title">{titleTwo}</h2>
      <p class="text-base-content text-opacity-60">{textTwo}</p>
    </div>
  </div>
</div>
