<!-- Authors: Idrees, Bhavya -->
<script lang="ts">
  import { afterUpdate } from 'svelte'
  import Chart from 'chart.js/auto'

  export let data: number[]
  export let labels: string[]

  let myChart: Chart

  const createChart = () => {
    if (myChart) {
      myChart.destroy()
    }

    const canvas: any = document.getElementById('myChart')
    const ctx = canvas.getContext('2d')
    myChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Performance',
            data: data,
            backgroundColor: 'rgba(0, 150, 255, 0.3)',
            borderColor: 'rgba(0, 150, 255, 1)',
            borderWidth: 1,
            fill: true,
            pointBackgroundColor: 'rgba(0, 150, 255, 1)',
          },
        ],
      },
      options: {
        plugins: {
          legend: {
            display: false,
          },
        },
        scales: {
          y: {
            title: { display: true, text: 'Performance' },
            beginAtZero: true,
          },
          x: {
            title: { display: true, text: 'Model Version' },
            beginAtZero: true,
          },
        },
      },
    })
  }

  afterUpdate(createChart)
</script>

<canvas id="myChart" width="300" height="100" />
