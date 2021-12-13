<script lang="ts">
  import { Classification } from '../Api'

  export let imgSrc: string =
    'https://images.unsplash.com/photo-1528821128474-27f963b062bf?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80'
  export let mlResponse: Classification | null
</script>

<div class="card bg-base-100 lg:h-96">
  <div class="card-body flex lg:flex-row lg:gap-x-10 gap-y-5">
    <div class="lg:h-80 w-full lg:w-1/2">
      <img
        class="rounded-xl h-full w-full object-cover"
        src={imgSrc}
        alt="img"
      />
    </div>

    <div
      class={`flex-grow flex-col flex ${
        !mlResponse && 'items-center justify-center'
      }`}
    >
      {#if mlResponse}
        <h1 class="card-title">Image Information</h1>
        <div>
          <b>Name:</b>
          <span>{mlResponse?.name}</span>
        </div>
        <div>
          <b>Type:</b>
          <span>{mlResponse?.type}</span>
        </div>
        <div>
          <b>Is Fresh:</b>
          <span>{mlResponse?.fresh}</span>
        </div>
      {:else}
        <p>Please Upload An Image to Classify</p>
      {/if}
    </div>
  </div>
</div>
