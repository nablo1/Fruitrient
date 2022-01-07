<!-- Authors: Idrees-->
<script>
  import { Link } from 'svelte-navigator'
</script>

<div class="navbar shadow-lg bg-neutral text-neutral-content rounded-box">
  <Link to="/" class="flex-1 px-2 mx-2">
    <span class="text-lg font-bold uppercase">Fruitrient</span>
  </Link>
  <div class="flex-none">
    <ul class="menu horizontal">
      <li>
        <Link to="/user" class="rounded-btn">User</Link>
      </li>
      <li>
        <Link to="/admin" class="rounded-btn">Admin</Link>
      </li>
    </ul>
  </div>
</div>
