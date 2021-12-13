<script>
  import { createEventDispatcher } from 'svelte'
  import { decode } from 'base64-arraybuffer'

  let stream
  let video
  let canvas
  let url

  const dispatch = createEventDispatcher()

  const requestAccess = async () => {
    try {
      stream = await navigator.mediaDevices.getUserMedia({ video: true })
      video.srcObject = stream
      video.play()
    } catch (error) {
      alert(`Failed to request camera access: ${error}`)
    }
  }

  const captureImage = () => {
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height)
    url = canvas.toDataURL('image/jpeg')
    closeWebcam()
  }

  const deleteImage = () => {
    url = null
  }

  const uploadImage = () => {
    const byteArray = decode(url)
    if (url) {
      dispatch('fileLoaded', {
        binary: byteArray,
        imaSrc: url,
      })
    }
    url = null
  }

  const closeWebcam = async () => {
    stream.getTracks().forEach(function (track) {
      if (track.readyState == 'live') {
        track.stop()
      }
    })
    stream = null
    video.srcObject = stream
  }
</script>

<div class="card compact bg-base-150">
  <h2 class="my-4 card-title text-center text-2xl font-bold card-title">
    Use Webcam
  </h2>

  <div>
    <div class="justify-center card-actions">
      {#if stream}
        <button on:click={captureImage} class="btn btn-outline btn-accent"
          >Capture Image</button
        >
        <button on:click={closeWebcam} class="btn btn-outline btn-accent"
          >Turn Off Webcam</button
        >
      {:else if !url}
        <button on:click={requestAccess} class="btn btn-outline btn-accent"
          >Start Webcam</button
        >
      {/if}
      {#if url}
        <div class="justify-center card-actions">
          <button on:click={uploadImage} class="btn btn-outline btn-accent"
            >Upload Image</button
          >
          <button on:click={deleteImage} class="btn btn-outline btn-accent"
            >Delete Image</button
          >
        </div>
        <div class="justify-center card-actions h-5/6 w-5/6">
          <img src={url} alt="Captured media" />
        </div>
      {:else}
        <div class="justify-center card-actions display-block w-5/6">
          <video bind:this={video} track kind="captions">
            />
            <track kind="captions" />
            <canvas style="display: flex;" bind:this={canvas} />
          </video>
        </div>
      {/if}
    </div>
  </div>
</div>
