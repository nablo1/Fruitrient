<script lang="ts">
  import { Router, Route } from 'svelte-navigator'
  import User from './pages/User.svelte'
  import Admin from './pages/Admin.svelte'
  import Home from './pages/Home.svelte'
  import Recipe from './pages/Recipe.svelte'
</script>

<main class="">
  <Router>
    <Route path="/">
      <Home />
    </Route>

    <Route path="user">
      <User />
    </Route>

    <Route path="admin">
      <Admin />
    </Route>
    <Route path="recipe/:id">
      <Recipe />
    </Route>
  </Router>
</main>

<style lang="postcss" global>
  @tailwind base;
  @tailwind components;
  @tailwind utilities;
</style>
