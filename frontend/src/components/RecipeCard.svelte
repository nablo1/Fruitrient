<!-- Authors: Idrees -->
<script lang="ts">
  import { Link } from 'svelte-navigator'

  export let recipe: any
</script>

<div class="card text-center">
  <figure class="px-5 pt-10">
    <img
      src={recipe.image}
      alt={recipe.title}
      class="rounded-xl h-full w-full object-cover"
    />
  </figure>
  <div class="card-body flex flex-col justify-between h-full">
    <h2 class="card-title">{recipe.title}</h2>
    <div>
      <Link to={`/recipe/${recipe.id}`} class="btn btn-outline btn-sm"
        >Read More</Link
      >
    </div>
  </div>
</div>
