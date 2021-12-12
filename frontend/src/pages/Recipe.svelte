<script lang="ts">
  import { navigate } from 'svelte-navigator'
  import { RecipesWithIngredient } from '../types'
  import recipeStore from '../store/store'
  import { useParams } from 'svelte-navigator'

  const params = useParams()

  let recipe: RecipesWithIngredient

  recipeStore.subscribe((data) => {
    recipe = data.filter((e) => e.id !== $params!.id).pop()
  })
</script>

<div class="w-2/4 mx-auto text-center mt-12">
  <button
    on:click={() => navigate(-1)}
    class="btn btn-outline btn-sm absolute top-16 left-16"
    ><svg
      width="24"
      height="24"
      fill-rule="evenodd"
      clip-rule="evenodd"
      viewBox="0 0 24 24"
      class="inline-block w-6 h-6 mr-2 stroke-current"
      ><path
        d="M2.117 12l7.527 6.235-.644.765-9-7.521 9-7.479.645.764-7.529 6.236h21.884v1h-21.883z"
      /></svg
    >
    back
  </button>
  <div class="flex flex-col items-center">
    <h1 class=" mb-10 text-4xl font-medium">{recipe.title}</h1>
    <img
      class="w-full h-full max-h-96 max-w-2xl object-cover mb-10"
      src={recipe.image}
      alt={recipe.title}
    />
    <div class="mb-10">
      <h1 class="text-left text-3xl font-medium mb-2">Summary</h1>
      <p class="text-justify">
        {@html recipe.summary}
      </p>
    </div>
    <div class="w-full mb-10">
      <h1 class="text-left text-3xl font-medium mb-2">Ingredients</h1>
      {#each recipe.extendedIngredients as ing}
        <div class="flex justify-between border-b pb-0 mb-2 border-dashed">
          <span class="capitalize">{ing.name}</span>
          <span
            >{ing.measures.metric.amount.toFixed(0)}
            {ing.measures.metric.unitShort}</span
          >
        </div>
      {/each}
    </div>
    {#if recipe.analyzedInstructions.length}
      <div class="w-full mb-10">
        <h1 class="text-left text-3xl font-medium mb-2">Instraction</h1>
        <ol class="text-left ml-5">
          {#each recipe.analyzedInstructions[0].steps as step}
            <li type="1">{step.step}</li>
          {/each}
        </ol>
      </div>
    {:else if recipe.instructions}
      <div class="mb-10">
        <h1 class="text-left text-3xl font-medium mb-2">Instraction</h1>
        <p class="text-justify">
          {@html recipe.instructions}
        </p>
      </div>
    {/if}
    <div class="w-full mb-10">
      <h1 class="text-left text-3xl font-medium mb-2">At Glance:</h1>
      <div class="flex justify-between border-b pb-0 mb-2 border-dashed">
        <span class="capitalize">Serving</span>
        <span>{recipe.servings}</span>
      </div>
      <div class="flex justify-between border-b pb-0 mb-2 border-dashed">
        <span class="capitalize">Price Per Serving</span>
        <span>{recipe.pricePerServing}</span>
      </div>
      <div class="flex justify-between border-b pb-0 mb-2 border-dashed">
        <span class="capitalize">Preparation Time</span>
        <span>{recipe.readyInMinutes} minutes</span>
      </div>
      <div class="flex justify-between border-b pb-0 mb-2 border-dashed">
        <span class="capitalize">vegan</span>
        <span>{recipe.vegan ? 'Yes' : 'No'}</span>
      </div>
      <div class="flex justify-between border-b pb-0 mb-2 border-dashed">
        <span class="capitalize">vegetarian</span>
        <span>{recipe.vegetarian ? 'Yes' : 'No'}</span>
      </div>
      <div class="flex justify-between border-b pb-0 mb-2 border-dashed">
        <span class="capitalize">dairy Free</span>
        <span>{recipe.dairyFree ? 'Yes' : 'No'}</span>
      </div>
      <div class="flex justify-between border-b pb-0 mb-2 border-dashed">
        <span class="capitalize">gluten Free</span>
        <span>{recipe.glutenFree ? 'Yes' : 'No'}</span>
      </div>
      <div class="flex justify-between border-b pb-0 mb-2 border-dashed">
        <span class="capitalize">ketogenic</span>
        <span>{recipe.ketogenic ? 'Yes' : 'No'}</span>
      </div>
      <div class="flex justify-between border-b pb-0 mb-2 border-dashed">
        <span class="capitalize">low Fodmap</span>
        <span>{recipe.lowFodmap ? 'Yes' : 'No'}</span>
      </div>
      <div class="flex justify-between border-b pb-0 mb-2 border-dashed">
        <span class="capitalize">sustainable</span>
        <span>{recipe.sustainable ? 'Yes' : 'No'}</span>
      </div>
    </div>
    <p class="text-left mb-10">
      <b>By:</b>
      <a class="link link-neutral" href={recipe.sourceUrl}
        >{recipe.creditsText}</a
      >
    </p>
  </div>
</div>
