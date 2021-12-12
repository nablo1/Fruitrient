export interface EstimatedCost {
  value: number
  unit: string
}

export interface Nutrient {
  title: string
  name: string
  amount: number
  unit: string
}

export interface Property {
  name: string
  title: string
  amount: number
  unit: string
}

export interface Flavonoid {
  name: string
  title: string
  amount: number
  unit: string
}

export interface CaloricBreakdown {
  percentProtein: number
  percentFat: number
  percentCarbs: number
}

export interface WeightPerServing {
  amount: number
  unit: string
}

export interface Nutrition {
  nutrients: Nutrient[]
  properties: Property[]
  flavonoids: Flavonoid[]
  caloricBreakdown: CaloricBreakdown
  weightPerServing: WeightPerServing
}

export interface NutritionFact {
  id: number
  original: string
  originalName: string
  name: string
  amount: number
  unit: string
  unitShort: string
  unitLong: string
  possibleUnits: string[]
  estimatedCost: EstimatedCost
  consistency: string
  shoppingListUnits: string[]
  aisle: string
  image: string
  meta: any[]
  nutrition: Nutrition
  categoryPath: string[]
}

export interface Us {
  amount: number
  unitShort: string
  unitLong: string
}

export interface Metric {
  amount: number
  unitShort: string
  unitLong: string
}

export interface Measures {
  us: Us
  metric: Metric
}

export interface ExtendedIngredient {
  id?: number
  aisle: string
  image: string
  consistency: string
  name: string
  nameClean: string
  original: string
  originalString: string
  originalName: string
  amount: number
  unit: string
  meta: string[]
  metaInformation: string[]
  measures: Measures
}

export interface WinePairing {
  pairedWines: any[]
  pairingText: string
  productMatches: any[]
}

export interface Ingredient {
  id: number
  name: string
  localizedName: string
  image: string
}

export interface Equipment {
  id: number
  name: string
  localizedName: string
  image: string
}

export interface Length {
  number: number
  unit: string
}

export interface Step {
  number: number
  step: string
  ingredients: Ingredient[]
  equipment: Equipment[]
  length: Length
}

export interface AnalyzedInstruction {
  name: string
  steps: Step[]
}

export interface RecipesWithIngredient {
  vegetarian?: boolean
  vegan?: boolean
  glutenFree?: boolean
  ketogenic?: boolean
  dairyFree?: boolean
  veryHealthy?: boolean
  cheap?: boolean
  veryPopular?: boolean
  sustainable?: boolean
  weightWatcherSmartPoints?: number
  gaps?: string
  lowFodmap?: boolean
  aggregateLikes: number
  spoonacularScore: number
  healthScore: number
  creditsText: string
  license?: string
  sourceName?: string
  pricePerServing?: number
  extendedIngredients: ExtendedIngredient[]
  id: number
  title: string
  author: string
  readyInMinutes: number
  servings: number
  sourceUrl?: string
  image: string
  imageType: string
  summary: string
  cuisines: any[]
  dishTypes: string[]
  diets: string[]
  occasions: any[]
  winePairing: WinePairing
  instructions: string
  analyzedInstructions: AnalyzedInstruction[]
  originalId?: any
  spoonacularSourceUrl: string
}
