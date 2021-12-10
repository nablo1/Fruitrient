<script>
  import { onMount } from 'svelte'
	import { navigate } from "svelte-navigator";
  const recipe = {
    vegetarian: true,
    vegan: false,
    glutenFree: true,
    dairyFree: false,
    veryHealthy: false,
    cheap: false,
    veryPopular: false,
    sustainable: false,
    weightWatcherSmartPoints: 17,
    gaps: 'no',
    lowFodmap: false,
    aggregateLikes: 2,
    spoonacularScore: 38,
    healthScore: 6,
    creditsText: 'Foodista.com – The Cooking Encyclopedia Everyone Can Edit',
    license: 'CC BY 3.0',
    sourceName: 'Foodista',
    pricePerServing: 61.47,
    extendedIngredients: [
      {
        id: 10120052,
        aisle: 'Pasta and Rice',
        image: 'uncooked-white-rice.png',
        consistency: 'solid',
        name: 'short grain rice',
        nameClean: 'short grain rice',
        original: '3/4 cup medium grain rice or short grain rice',
        originalString: '3/4 cup medium grain rice or short grain rice',
        originalName: 'grain rice or short grain rice',
        amount: 0.75,
        unit: 'cup',
        meta: ['medium grain'],
        metaInformation: ['medium grain'],
        measures: {
          us: { amount: 0.75, unitShort: 'cups', unitLong: 'cups' },
          metric: { amount: 177.441, unitShort: 'ml', unitLong: 'milliliters' },
        },
      },
      {
        id: 14412,
        aisle: 'Beverages',
        image: 'water.png',
        consistency: 'liquid',
        name: 'water',
        nameClean: 'water',
        original: '1 1/2 cups water',
        originalString: '1 1/2 cups water',
        originalName: 'water',
        amount: 1.5,
        unit: 'cups',
        meta: [],
        metaInformation: [],
        measures: {
          us: { amount: 1.5, unitShort: 'cups', unitLong: 'cups' },
          metric: { amount: 354.882, unitShort: 'ml', unitLong: 'milliliters' },
        },
      },
      {
        id: 2047,
        aisle: 'Spices and Seasonings',
        image: 'salt.jpg',
        consistency: 'solid',
        name: 'salt',
        nameClean: 'salt',
        original: '1/4 teaspoon salt (heaping)',
        originalString: '1/4 teaspoon salt (heaping)',
        originalName: 'salt (heaping)',
        amount: 0.25,
        unit: 'teaspoon',
        meta: ['()'],
        metaInformation: ['()'],
        measures: {
          us: { amount: 0.25, unitShort: 'tsps', unitLong: 'teaspoons' },
          metric: { amount: 0.25, unitShort: 'tsps', unitLong: 'teaspoons' },
        },
      },
      {
        id: 1077,
        aisle: 'Milk, Eggs, Other Dairy',
        image: 'milk.png',
        consistency: 'liquid',
        name: 'whole milk',
        nameClean: 'milk',
        original: '4 cups whole milk (I use 2%%)',
        originalString: '4 cups whole milk (I use 2%%)',
        originalName: 'whole milk (I use 2%%)',
        amount: 4,
        unit: 'cups',
        meta: ['whole', '(I use 2%%)'],
        metaInformation: ['whole', '(I use 2%%)'],
        measures: {
          us: { amount: 4, unitShort: 'cups', unitLong: 'cups' },
          metric: { amount: 946.352, unitShort: 'ml', unitLong: 'milliliters' },
        },
      },
      {
        id: 19335,
        aisle: 'Baking',
        image: 'sugar-in-bowl.png',
        consistency: 'solid',
        name: 'sugar',
        nameClean: 'sugar',
        original: '1/2 cup sugar',
        originalString: '1/2 cup sugar',
        originalName: 'sugar',
        amount: 0.5,
        unit: 'cup',
        meta: [],
        metaInformation: [],
        measures: {
          us: { amount: 0.5, unitShort: 'cups', unitLong: 'cups' },
          metric: { amount: 118.294, unitShort: 'ml', unitLong: 'milliliters' },
        },
      },
      {
        id: 2050,
        aisle: 'Baking',
        image: 'vanilla-extract.jpg',
        consistency: 'liquid',
        name: 'vanilla',
        nameClean: 'vanilla extract',
        original: '1/2 teaspoon vanilla',
        originalString: '1/2 teaspoon vanilla',
        originalName: 'vanilla',
        amount: 0.5,
        unit: 'teaspoon',
        meta: [],
        metaInformation: [],
        measures: {
          us: { amount: 0.5, unitShort: 'tsps', unitLong: 'teaspoons' },
          metric: { amount: 0.5, unitShort: 'tsps', unitLong: 'teaspoons' },
        },
      },
      {
        id: 1123,
        aisle: 'Milk, Eggs, Other Dairy',
        image: 'egg.png',
        consistency: 'solid',
        name: 'egg',
        nameClean: 'egg',
        original: '1 egg, beaten',
        originalString: '1 egg, beaten',
        originalName: 'egg, beaten',
        amount: 1,
        unit: '',
        meta: ['beaten'],
        metaInformation: ['beaten'],
        measures: {
          us: { amount: 1, unitShort: '', unitLong: '' },
          metric: { amount: 1, unitShort: '', unitLong: '' },
        },
      },
      {
        id: 1001,
        aisle: 'Milk, Eggs, Other Dairy',
        image: 'butter-sliced.jpg',
        consistency: 'solid',
        name: 'butter',
        nameClean: 'butter',
        original: '1 teaspoon butter',
        originalString: '1 teaspoon butter',
        originalName: 'butter',
        amount: 1,
        unit: 'teaspoon',
        meta: [],
        metaInformation: [],
        measures: {
          us: { amount: 1, unitShort: 'tsp', unitLong: 'teaspoon' },
          metric: { amount: 1, unitShort: 'tsp', unitLong: 'teaspoon' },
        },
      },
      {
        id: 2010,
        aisle: 'Spices and Seasonings',
        image: 'cinnamon.jpg',
        consistency: 'solid',
        name: 'cinnamon',
        nameClean: 'cinnamon',
        original: '1 pinch cinnamon',
        originalString: '1 pinch cinnamon',
        originalName: 'cinnamon',
        amount: 1,
        unit: 'pinch',
        meta: [],
        metaInformation: [],
        measures: {
          us: { amount: 1, unitShort: 'pinch', unitLong: 'pinch' },
          metric: { amount: 1, unitShort: 'pinch', unitLong: 'pinch' },
        },
      },
      {
        id: 2025,
        aisle: 'Spices and Seasonings',
        image: 'ground-nutmeg.jpg',
        consistency: 'solid',
        name: 'nutmeg',
        nameClean: 'nutmeg',
        original: 'pinch nutmeg',
        originalString: 'pinch nutmeg',
        originalName: 'pinch nutmeg',
        amount: 1,
        unit: 'pinch',
        meta: [],
        metaInformation: [],
        measures: {
          us: { amount: 1, unitShort: 'pinch', unitLong: 'pinch' },
          metric: { amount: 1, unitShort: 'pinch', unitLong: 'pinch' },
        },
      },
    ],
    id: 658276,
    title: 'Rice Pudding',
    readyInMinutes: 45,
    servings: 4,
    sourceUrl: 'https://www.foodista.com/recipe/C75THTG5/rice-pudding',
    image: 'https://spoonacular.com/recipeImages/658276-556x370.jpg',
    imageType: 'jpg',
    summary:
      'If you have around <b>about 45 minutes</b> to spend in the kitchen, Rice Pudding might be a super <b>gluten free and lacto ovo vegetarian</b> recipe to try. One serving contains <b>407 calories</b>, <b>12g of protein</b>, and <b>10g of fat</b>. This recipe serves 4. For <b>61 cents per serving</b>, this recipe <b>covers 14%</b> of your daily requirements of vitamins and minerals. A mixture of short grain rice, water, milk, and a handful of other ingredients are all it takes to make this recipe so flavorful. This recipe is liked by 2 foodies and cooks. It works well as a dessert. It is brought to you by Foodista. Overall, this recipe earns a <b>not so awesome spoonacular score of 36%</b>. Similar recipes include <a href="https://spoonacular.com/recipes/left-over-rice-make-rice-pudding-532769">Left over rice? Make Rice pudding</a>, <a href="https://spoonacular.com/recipes/rice-kheer-rice-pudding-600368">Rice Kheer (Rice Pudding)</a>, and <a href="https://spoonacular.com/recipes/brown-rice-rice-pudding-79963">Brown Rice Rice Pudding</a>.',
    cuisines: [],
    dishTypes: ['dessert'],
    diets: ['gluten free', 'lacto ovo vegetarian'],
    occasions: [],
    winePairing: {
      pairedWines: ['cream sherry', 'moscato dasti', 'port'],
      pairingText:
        "Cream Sherry, Moscato d'Asti, and Port are great choices for Rice Pudding. A common wine pairing rule is to make sure your wine is sweeter than your food. Delicate desserts go well with Moscato d'Asti, nutty desserts with cream sherry, and caramel or chocolate desserts pair well with port. The NV Solera Cream Sherry with a 4.5 out of 5 star rating seems like a good match. It costs about 17 dollars per bottle.",
      productMatches: [
        {
          id: 428475,
          title: 'NV Solera Cream Sherry',
          description:
            'The Solera Cream Sherry has a brilliant amber and deep copper hue. With butterscotch and pecan aromas, the sweet salted nut and brown spice aromas carry a complex caramel accent. A sweet entry leads to a rounded, lush, moderately full-bodied palate with a lengthy, flavorful finish.',
          price: '$16.99',
          imageUrl: 'https://spoonacular.com/productImages/428475-312x231.jpg',
          averageRating: 0.9,
          ratingCount: 4,
          score: 0.823076923076923,
          link: 'https://www.amazon.com/NV-Solera-Cream-Sherry-750/dp/B00HSME8OW?tag=spoonacular-20',
        },
      ],
    },
    instructions:
      'In a medium saucepan, bring 1 1/2 cups water to a boil. Add rice, salt and stir.\nSimmer covered until water has been absorbed (approximately 15 minutes).\nIn another sauce pan, stir in 1 1/2 milk, sugar, and 1 1/2 cups cooked rice, cook over medium heat\nStir constantly until thick and creamy, for 15 to 20 minutes.\nCombine 1/2 cup milk, and beaten egg, then add to saucepan. Cook 2 minutes more, stirring constantly\nRemove from heat, Add in butter, and vanilla.\nSeason with a pinch of nutmeg or cinnamon.\nServe warm.',
    analyzedInstructions: [
      {
        name: '',
        steps: [
          {
            number: 1,
            step: 'In a medium saucepan, bring 1 1/2 cups water to a boil.',
            ingredients: [
              {
                id: 14412,
                name: 'water',
                localizedName: 'water',
                image: 'water.png',
              },
            ],
            equipment: [
              {
                id: 404669,
                name: 'sauce pan',
                localizedName: 'sauce pan',
                image: 'sauce-pan.jpg',
              },
            ],
          },
          {
            number: 2,
            step: 'Add rice, salt and stir.',
            ingredients: [
              {
                id: 20444,
                name: 'rice',
                localizedName: 'rice',
                image: 'uncooked-white-rice.png',
              },
              {
                id: 2047,
                name: 'salt',
                localizedName: 'salt',
                image: 'salt.jpg',
              },
            ],
            equipment: [],
          },
          {
            number: 3,
            step: 'Simmer covered until water has been absorbed (approximately 15 minutes).',
            ingredients: [
              {
                id: 14412,
                name: 'water',
                localizedName: 'water',
                image: 'water.png',
              },
            ],
            equipment: [],
            length: { number: 15, unit: 'minutes' },
          },
          {
            number: 4,
            step: 'In another sauce pan, stir in 1 1/2 milk, sugar, and 1 1/2 cups cooked rice, cook over medium heat',
            ingredients: [
              {
                id: 10220445,
                name: 'cooked rice',
                localizedName: 'cooked rice',
                image: 'uncooked-white-rice.png',
              },
              { id: 0, name: 'sauce', localizedName: 'sauce', image: '' },
              {
                id: 19335,
                name: 'sugar',
                localizedName: 'sugar',
                image: 'sugar-in-bowl.png',
              },
              {
                id: 1077,
                name: 'milk',
                localizedName: 'milk',
                image: 'milk.png',
              },
            ],
            equipment: [
              {
                id: 404669,
                name: 'sauce pan',
                localizedName: 'sauce pan',
                image: 'sauce-pan.jpg',
              },
            ],
          },
          {
            number: 5,
            step: 'Stir constantly until thick and creamy, for 15 to 20 minutes.',
            ingredients: [],
            equipment: [],
            length: { number: 15, unit: 'minutes' },
          },
          {
            number: 6,
            step: 'Combine 1/2 cup milk, and beaten egg, then add to saucepan. Cook 2 minutes more, stirring constantly',
            ingredients: [
              {
                id: 1077,
                name: 'milk',
                localizedName: 'milk',
                image: 'milk.png',
              },
              { id: 1123, name: 'egg', localizedName: 'egg', image: 'egg.png' },
            ],
            equipment: [
              {
                id: 404669,
                name: 'sauce pan',
                localizedName: 'sauce pan',
                image: 'sauce-pan.jpg',
              },
            ],
            length: { number: 2, unit: 'minutes' },
          },
          {
            number: 7,
            step: 'Remove from heat,',
            ingredients: [],
            equipment: [],
          },
          {
            number: 8,
            step: 'Add in butter, and vanilla.',
            ingredients: [
              {
                id: 1052050,
                name: 'vanilla',
                localizedName: 'vanilla',
                image: 'vanilla.jpg',
              },
              {
                id: 1001,
                name: 'butter',
                localizedName: 'butter',
                image: 'butter-sliced.jpg',
              },
            ],
            equipment: [],
          },
          {
            number: 9,
            step: 'Season with a pinch of nutmeg or cinnamon.',
            ingredients: [
              {
                id: 2010,
                name: 'cinnamon',
                localizedName: 'cinnamon',
                image: 'cinnamon.jpg',
              },
              {
                id: 2025,
                name: 'nutmeg',
                localizedName: 'nutmeg',
                image: 'ground-nutmeg.jpg',
              },
            ],
            equipment: [],
          },
          { number: 10, step: 'Serve warm.', ingredients: [], equipment: [] },
        ],
      },
    ],
    originalId: null,
    spoonacularSourceUrl: 'https://spoonacular.com/rice-pudding-658276',
  }

  onMount(() => {})
</script>

<div class="w-2/4 mx-auto text-center mt-12">
  <button on:click="{() => navigate(-1)}" class="btn btn-outline btn-sm absolute top-16 left-16"
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
