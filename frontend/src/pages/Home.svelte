<!-- Author: Idrees  -->
<script>
  import { Link } from 'svelte-navigator'
</script>

<div
  style="background-image: url(assets/bg.jpg);"
  class="hero min-h-screen bg-base-200 relative"
>
  <Link to="/" class="absolute top-4 left-4 text-2xl">Fruitrient</Link>
  <div class="text-center hero-content">
    <div class="max-w-md">
      <h1 class="mb-5 text-6xl font-bold">Fruitrient</h1>
      <p class="text-1xl mb-5">
        The only tool you need in your fail attempts to eat healthy
      </p>
      <Link to="admin" class="btn btn-outline">use as admin</Link>
      <Link to="user" class="btn px-6">use as user</Link>
    </div>
  </div>
</div>