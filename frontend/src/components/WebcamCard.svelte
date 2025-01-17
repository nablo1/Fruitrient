<!-- Authors: Idrees, Bhavya, Rughter, Rilind -->
<script lang="ts">
  import { createEventDispatcher } from 'svelte'
  import { decode } from 'base64-arraybuffer'

  let stream: MediaStream | null = null
  let video: HTMLVideoElement
  let canvas: HTMLCanvasElement
  let url: string | null = null

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
    canvas.getContext('2d')!.drawImage(video, 0, 0, canvas.width, canvas.height)
    url = canvas.toDataURL('image/jpeg')
    closeWebcam()
  }

  const deleteImage = () => {
    url = null
  }

  const uploadImage = () => {
    if (!url) {
      console.log('error: no data url to upload')
      return
    }

    const base64 = url.substring(url.indexOf(',') + 1)

    const byteArray = decode(base64)
    if (url) {
      dispatch('fileLoaded', {
        binary: byteArray,
        imaSrc: url,
      })
    }
    url = null
  }

  const closeWebcam = async () => {
    stream?.getTracks().forEach(function (track) {
      if (track.readyState == 'live') {
        track.stop()
      }
    })
    stream = null
    video.srcObject = stream
  }
</script>

<div class="card compact bg-base-150">
  <h2 class="my-2 card-title text-center text-2xl font-bold card-title">
    Use Webcam
  </h2>

  <div>
    <div class="justify-center card-actions">
      {#if url}
        <div class="justify-center h-5/6 w-5/6">
          <img src={url} alt="Captured media" />
        </div>
        <div class="justify-center mb-0">
          <button on:click={uploadImage} class="btn btn-outline btn-sm"
            >Upload Image</button
          >
          <button on:click={deleteImage} class="btn btn-outline btn-sm"
            >Delete Image</button
          >
        </div>
      {:else}
        <div class="justify-center display-block w-5/6">
          <video bind:this={video} kind="captions">
            />
            <track kind="captions" />
            <canvas class="flex" bind:this={canvas} />
          </video>
        </div>
      {/if}
            {#if stream}
        <button on:click={captureImage} class="btn btn-outline btn-sm"
          >Capture Image</button
        >
        <button on:click={closeWebcam} class="btn btn-outline btn-sm"
          >Turn Off Webcam</button
        >
      {:else if !url}
        <button on:click={requestAccess} class="btn btn-outline btn-sm"
          >Start Webcam</button
        >
      {/if}
    </div>
  </div>
</div>
