<script>
  import { Link } from 'svelte-navigator'
</script>

<div
  style="background-image: url(assets/bg.jpg);"
  class="hero min-h-screen bg-base-200 relative"
>
  <Link to="/" class="absolute top-4 left-4 text-2xl">fruitrient</Link>
  <div class="text-center hero-content">
    <div class="max-w-md">
      <h1 class="mb-5 text-5xl font-bold">fruitrient</h1>
      <p class="mb-5">
        the only tool you need in your fail attempts to eat healthy
      </p>
      <Link to="admin" class="btn btn-primary lowercase">use as admin</Link>
      <Link to="user" class="btn btn-primary lowercase px-6">use as user</Link>
    </div>
  </div>
</div>
