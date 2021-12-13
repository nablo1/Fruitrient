<script lang="ts">
  // components
  import FileUpload from '../components/FileUpload.svelte'
  import InfoCard from '../components/InfoCard.svelte'
  import NavBar from '../components/NavBar.svelte'
  import NutritionCard from '../components/NutritionCard.svelte'
  import RecipeCard from '../components/RecipeCard.svelte'
  import WebcamCard from '../components/WebcamCard.svelte'
  import CapturedImageCard from '../components/CapturedImageCard.svelte'
  import recipeStore from '../store/store'

  import {
    Classification,
    classify,
    nutrition_facts,
    Prediction,
    predictions,
    recipes_with_ingredient,
  } from '../Api'
  import { Link } from 'svelte-navigator'
  import { onMount } from 'svelte'
  import { NutritionFact, RecipesWithIngredient } from '../types'

  let imgSrc: string | undefined
  let mlResponse: Classification | null
  let nutration: NutritionFact | null
  let recipes: RecipesWithIngredient[] | null
  let lastPredection: Prediction[]

  const imageLoaded = async (data: CustomEvent) => {
    mlResponse = await classify(new Uint8Array(data.detail.binary))
    imgSrc = data.detail.imaSrc
    //! uncomment before deploy

    // const nutritionFacts = await nutrition_facts(
    //   lastPredection[0]?.name || 'apple'
    // )
    // recipes = await recipes_with_ingredient(lastPredection[0]?.name || 'apple')
    // nutration = nutritionFacts!.nutrition

    // recipeStore.update((prevData) => {
    //   if (recipes && recipes.length) return [...prevData, ...recipes]
    //   return prevData
    // })
  }

  const webcamUpload = async (data: CustomEvent) => {
    mlResponse = await classify(data.detail.binary)
    imgSrc = data.detail.imaSrc
  }

  onMount(async () => {
    lastPredection = await predictions()
    //! uncomment before deploy
    // imgSrc = lastPredection[0]?.image
    // const nutritionFacts = await nutrition_facts(
    //   lastPredection[0]?.name || 'apple'
    // )
    // recipes = await recipes_with_ingredient(lastPredection[0]?.name || 'apple')
    // nutration = nutritionFacts!.nutrition

    // recipeStore.update((prevData) => {
    //   if (recipes && recipes.length) return [...prevData, ...recipes]
    //   return prevData
    // })
  })
</script>

<div
  class="grid grid-cols-1 gap-6 p-10 xl:grid-cols-9 lg:bg-base-200 rounded-box"
>
  <div class="col-span-1 xl:col-span-9 shadow-lg">
    <NavBar />
  </div>
  <div
    class="col-span-1 row-span-3 shadow-lg xl:col-span-3 bg-base-100 rounded-box"
  >
    <InfoCard />
  </div>
  <div class="row-span-3 shadow-lg xl:col-span-3 bg-base-100 rounded-box">
    <FileUpload
      on:fileLoaded={imageLoaded}
      title="Upload an Image"
      fileType="image/*"
      uploadText="Drop an Image, or click to select an image"
    />
  </div>
  <div class="shadow-lg row-span-3 xl:col-span-3 bg-base-100 rounded-box">
    <WebcamCard on:fileLoaded={webcamUpload} />
  </div>
  <div class="col-span-1 row-span-1 shadow-lg xl:col-span-6 rounded-box">
    <CapturedImageCard {imgSrc} {mlResponse} />
  </div>
  <div
    class="shadow-lg row-span-2  xl:col-span-3 bg-base-100  rounded-box max-h-[49rem]  overflow-y-auto"
  >
    {#if nutration}
      <NutritionCard {nutration} />
    {/if}
  </div>
  {#if recipes && recipes.length}
    {#each recipes as recipe}
      <Link
        to={`/recipe/${recipe.id}`}
        class="shadow-lg xl:col-span-2 bg-base-100 rounded-box"
      >
        <RecipeCard {recipe} />
      </Link>
    {/each}
  {/if}
</div>
