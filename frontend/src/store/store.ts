import { writable } from 'svelte/store'

const recipeStore = writable([] as any[])

export default recipeStore
