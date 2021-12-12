<script lang="ts">
  export let nutration: any = undefined
</script>

<div class="card text-base-content text-opacity-40 rounded-box">
  <div class="card-body">
    <h2 class="card-title">Nutritions</h2>
    <div class="overflow-x-auto">
      <table class="table w-full table-compact">
        <thead>
          <tr>
            <th />
            <th>Name</th>
            <th>value</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <th>1</th>
            <td class="capitalize">calories</td>
            <td class="capitalize">{nutration.calories}</td>
          </tr>
          <tr>
            <th>2</th>
            <td class="capitalize">carbs</td>
            <td class="capitalize">{nutration.carbs}</td>
          </tr>
          <tr>
            <th>3</th>
            <td class="capitalize">fat</td>
            <td class="capitalize">{nutration.fat}</td>
          </tr>
          <tr>
            <th>4</th>
            <td class="capitalize">protein</td>
            <td class="capitalize">{nutration.protein}</td>
          </tr>
          <tr class="active">
            <th class="capitalize">good nutrients</th>
            <td class="capitalize" />
            <td class="capitalize" />
          </tr>
          {#each nutration.good as good, i}
            <tr>
              <th>{i + 5}</th>
              <td class="capitalize">{good.title}</td>
              <td class="capitalize">{good.amount}</td>
            </tr>
          {/each}
          <tr class="active rounded">
            <th class="capitalize">bad nutrients</th>
            <td class="capitalize" />
            <td class="capitalize" />
          </tr>
          {#each nutration.bad as bad, i}
            <tr>
              <th>{i + nutration.good.length + 5}</th>
              <td class="capitalize">{bad.title}</td>
              <td class="capitalize">{bad.amount}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </div>
</div>
