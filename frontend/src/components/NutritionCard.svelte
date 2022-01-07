<!-- Authors: Idrees, Bhavya -->
<script lang="ts">
  import { Nutrition } from '../types'

  export let nutration: Nutrition
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
            <td class="capitalize">{nutration.caloricBreakdown.percentCarbs}</td
            >
          </tr>
          <tr>
            <th>2</th>
            <td class="capitalize">fat</td>
            <td class="capitalize">{nutration.caloricBreakdown.percentFat}</td>
          </tr>
          <tr>
            <th>3</th>
            <td class="capitalize">protein</td>
            <td class="capitalize"
              >{nutration.caloricBreakdown.percentProtein}</td
            >
          </tr>
          <tr class="active">
            <th class="capitalize">nutrients</th>
            <td class="capitalize" />
            <td class="capitalize" />
          </tr>
          {#each nutration.nutrients as e, i}
            <tr>
              <th>{i + 4}</th>
              <td class="capitalize">{e.title}</td>
              <td class="capitalize">{e.amount}{e.unit}</td>
            </tr>
          {/each}
          <tr class="active rounded">
            <th class="capitalize">flavonoids</th>
            <td class="capitalize" />
            <td class="capitalize" />
          </tr>
          {#each nutration.flavonoids as e, i}
            <tr>
              <th>{i + nutration.nutrients.length + 4}</th>
              <td class="capitalize">{e.title}</td>
              <td class="capitalize">{e.amount}{e.unit}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </div>
</div>
