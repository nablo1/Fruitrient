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
  <div class="card-body">
    <h2 class="card-title">{recipe.title}</h2>
    <div class="justify-center card-actions">
      <Link to={`/recipe/${recipe.id}`} class="btn btn-outline btn-accent"
        >Read More</Link
      >
    </div>
  </div>
</div>
