<script>
  
  import { createEventDispatcher } from 'svelte'
  
  const dispatch = createEventDispatcher();
  let stream;
	let video;
	let canvas;
  let url;

    async function requestAccess() {
		try {
			stream = await navigator.mediaDevices.getUserMedia({ video: true });
			video.srcObject = stream;
            video.play();
		    } catch (error) {
			alert(`Failed to request camera access: ${error}`);
		}
	}
	
	function captureImage() {
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
		  canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
      url = canvas.toDataURL('image/jpeg');
	  }
</script>

<style>

  video {
    display: block;
    margin: 15px auto;
  }

</style>

<div class="card compact bg-base-150">
  <!--<figure><img src="https://picsum.photos/id/1005/600/400" alt="img" /></figure>-->
  <div class="flex-row items-center space-x-4 card-body">
    <div>
      {#if url}
      <div>
        <h1><button class="btn btn-outline btn-accent">Captured Media</button></h1>
        <img src={url} width="auto" height="auto" alt="Captured media" />
      </div>
      {/if}

      {#if stream}
        <button on:click={captureImage} class="btn btn-outline btn-accent">Capture Image</button>
        {:else}
        <button on:click={requestAccess} class="btn btn-outline btn-accent">Request Camera Access</button>
      {/if}
      <video bind:this={video} track kind="captions"> />
      <track kind="captions">
      <canvas style="display: none;" bind:this={canvas} />
      <h2> class="card-title">Use Camera</h2>
    </div>
  </div>
</div>
