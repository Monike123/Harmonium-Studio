let intervalId = null
let isRunning = false
let currentAudio = null
let isPlaying = false
let audioLoading = false
let imageLoading = false

// Track current files to avoid unnecessary reloads
let currentImageFile = null
let currentTuneFile = null

// Audio transition management
const fadeInterval = null
let nextAudio = null
let isTransitioning = false

// Synchronization state
let pendingImageFile = null
let pendingTuneFile = null
let waitingForAudioEnd = false

// Batch playback state
let totalImages = 0
let generationComplete = false
let tuneDuration = 15 // Default duration, will be updated from user input

// DOM elements
const elements = {
  startBtn: document.getElementById("startBtn"),
  stopBtn: document.getElementById("stopBtn"),
  duration: document.getElementById("duration"),
  time: document.getElementById("time"),
  count: document.getElementById("count"),
  remaining: document.getElementById("remaining"),
  slideImg: document.getElementById("slideImg"),
  audioPlayer: document.getElementById("audioPlayer"),
  playPauseBtn: document.getElementById("playPauseBtn"),
  playIcon: document.getElementById("playIcon"),
  pauseIcon: document.getElementById("pauseIcon"),
  progressFill: document.getElementById("progressFill"),
  currentTime: document.getElementById("currentTime"),
  totalTime: document.getElementById("totalTime"),
  mainContent: document.getElementById("mainContent"),
  welcomeMessage: document.getElementById("welcomeMessage"),
  loadingOverlay: document.getElementById("loadingOverlay"),
  errorToast: document.getElementById("errorToast"),
  errorMessage: document.getElementById("errorMessage"),
  closeError: document.getElementById("closeError"),
  imageLoader: document.getElementById("imageLoader"),
  audioLoader: document.getElementById("audioLoader"),
}

// Utility functions
function formatTime(seconds) {
  if (isNaN(seconds)) return "0:00"
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, "0")}`
}

function showError(message) {
  elements.errorMessage.textContent = message
  elements.errorToast.classList.remove("hidden")
  setTimeout(() => {
    elements.errorToast.classList.add("hidden")
  }, 5000)
}

function showLoading(show = true, message = "Generating harmonium tunes...") {
  if (show) {
    elements.loadingOverlay.classList.remove("hidden")
    elements.loadingOverlay.querySelector("p").textContent = message
  } else {
    elements.loadingOverlay.classList.add("hidden")
  }
}

function updateButtonStates() {
  elements.startBtn.disabled = isRunning
  elements.stopBtn.disabled = !isRunning

  if (isRunning) {
    elements.startBtn.classList.add("disabled")
    elements.stopBtn.classList.remove("disabled")
    elements.startBtn.innerHTML = `
      <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <div class="spinner"></div>
      </svg>
      Generating...
    `
  } else {
    elements.startBtn.classList.remove("disabled")
    elements.stopBtn.classList.add("disabled")
    elements.startBtn.innerHTML = `
      <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <polygon points="5,3 19,12 5,21"/>
      </svg>
      Start Generation
    `
  }
}

function updatePlayPauseButton() {
  if (audioLoading || isTransitioning) {
    elements.audioLoader.classList.remove("hidden")
    elements.playIcon.classList.add("hidden")
    elements.pauseIcon.classList.add("hidden")
    elements.playPauseBtn.disabled = true
  } else {
    elements.audioLoader.classList.add("hidden")
    elements.playPauseBtn.disabled = false

    if (isPlaying) {
      elements.playIcon.classList.add("hidden")
      elements.pauseIcon.classList.remove("hidden")
    } else {
      elements.playIcon.classList.remove("hidden")
      elements.pauseIcon.classList.add("hidden")
    }
  }
}

// Enhanced audio fade effects with automatic fade-out near end
function fadeOut(audio, duration = 1000) {
  return new Promise((resolve) => {
    if (!audio) {
      resolve()
      return
    }

    const startVolume = audio.volume
    const fadeStep = startVolume / (duration / 50)

    const fade = setInterval(() => {
      if (audio.volume > fadeStep) {
        audio.volume = Math.max(0, audio.volume - fadeStep)
      } else {
        audio.volume = 0
        audio.pause()
        clearInterval(fade)
        resolve()
      }
    }, 50)
  })
}

function fadeIn(audio, duration = 1000, targetVolume = 1.0) {
  return new Promise((resolve) => {
    if (!audio) {
      resolve()
      return
    }

    audio.volume = 0
    const fadeStep = targetVolume / (duration / 50)

    audio
      .play()
      .then(() => {
        const fade = setInterval(() => {
          if (audio.volume < targetVolume - fadeStep) {
            audio.volume = Math.min(targetVolume, audio.volume + fadeStep)
          } else {
            audio.volume = targetVolume
            clearInterval(fade)
            resolve()
          }
        }, 50)
      })
      .catch((error) => {
        console.error("Fade in play error:", error)
        resolve()
      })
  })
}

// Auto fade-out near end of track
function setupAutoFadeOut(audio) {
  if (!audio) return

  const checkForFadeOut = () => {
    if (audio && audio.duration && audio.currentTime) {
      const timeRemaining = audio.duration - audio.currentTime
      // Start fade-out 2 seconds before the end
      if (timeRemaining <= 2 && timeRemaining > 0 && audio.volume > 0.1) {
        fadeOut(audio, 2000)
      }
    }
  }

  audio.addEventListener('timeupdate', checkForFadeOut)
}

// Audio management with smooth transitions and synchronization
function cleanupAudio() {
  if (currentAudio) {
    currentAudio.pause()
    currentAudio.removeEventListener("loadstart", handleAudioLoadStart)
    currentAudio.removeEventListener("canplay", handleAudioCanPlay)
    currentAudio.removeEventListener("play", handleAudioPlay)
    currentAudio.removeEventListener("pause", handleAudioPause)
    currentAudio.removeEventListener("ended", handleAudioEnded)
    currentAudio.removeEventListener("timeupdate", handleAudioTimeUpdate)
    currentAudio.removeEventListener("loadedmetadata", handleAudioLoadedMetadata)
    currentAudio.removeEventListener("error", handleAudioError)
    currentAudio.volume = 1.0
    currentAudio = null
  }

  if (nextAudio) {
    nextAudio.pause()
    nextAudio = null
  }

  isPlaying = false
  audioLoading = false
  isTransitioning = false
  waitingForAudioEnd = false
  pendingImageFile = null
  pendingTuneFile = null
  updatePlayPauseButton()
}

async function setupAudio(audioSrc) {
  if (isTransitioning) return

  isTransitioning = true
  audioLoading = true
  updatePlayPauseButton()

  // Create new audio element for next track
  nextAudio = new Audio()
  nextAudio.preload = "auto"
  nextAudio.src = audioSrc

  // Add event listeners to next audio
  nextAudio.addEventListener("loadedmetadata", () => {
    elements.totalTime.textContent = formatTime(nextAudio.duration)
  })

  nextAudio.addEventListener("error", () => {
    audioLoading = false
    isTransitioning = false
    updatePlayPauseButton()
    showError("Failed to load audio file")
  })

  try {
    // Load the next audio
    await new Promise((resolve, reject) => {
      nextAudio.addEventListener("canplaythrough", resolve, { once: true })
      nextAudio.addEventListener("error", reject, { once: true })
      nextAudio.load()
    })

    // Fade out current audio if playing
    if (currentAudio && isPlaying) {
      await fadeOut(currentAudio, 800)
    }

    // Switch to next audio
    if (currentAudio) {
      currentAudio.pause()
    }

    currentAudio = nextAudio
    nextAudio = null

    // Add event listeners to current audio
    currentAudio.addEventListener("play", handleAudioPlay)
    currentAudio.addEventListener("pause", handleAudioPause)
    currentAudio.addEventListener("ended", handleAudioEnded)
    currentAudio.addEventListener("timeupdate", handleAudioTimeUpdate)

    // Setup auto fade-out near end
    setupAutoFadeOut(currentAudio)

    audioLoading = false
    isTransitioning = false
    updatePlayPauseButton()

    // Auto-play with fade in if generation is running
    if (isRunning && generationComplete) {
      await fadeIn(currentAudio, 1000) // Longer fade-in for smoother start
    }
  } catch (error) {
    console.error("Audio setup error:", error)
    audioLoading = false
    isTransitioning = false
    updatePlayPauseButton()
    showError("Failed to load audio file")
  }
}

// Audio event handlers with synchronization logic
function handleAudioPlay() {
  isPlaying = true
  updatePlayPauseButton()
}

function handleAudioPause() {
  isPlaying = false
  updatePlayPauseButton()
}

function handleAudioEnded() {
  isPlaying = false
  updatePlayPauseButton()
  elements.progressFill.style.width = "0%"
  elements.currentTime.textContent = "0:00"
  
  // Handle synchronized transition when audio ends
  if (waitingForAudioEnd && pendingImageFile && pendingTuneFile) {
    waitingForAudioEnd = false
    
    // Update both image and tune simultaneously
    currentImageFile = pendingImageFile
    currentTuneFile = pendingTuneFile
    
    const imgSrc = `/image/${pendingImageFile}?${Date.now()}`
    const tuneSrc = `/tune/${pendingTuneFile}?${Date.now()}`
    
    // Setup image and audio simultaneously
    setupImage(imgSrc)
    setupAudio(tuneSrc)
    
    // Clear pending files
    pendingImageFile = null
    pendingTuneFile = null
  }
}

function handleAudioTimeUpdate() {
  if (currentAudio && currentAudio.duration) {
    const progress = (currentAudio.currentTime / currentAudio.duration) * 100
    elements.progressFill.style.width = `${progress}%`
    elements.currentTime.textContent = formatTime(currentAudio.currentTime)
  }
}

// Image handling with smooth transitions
function handleImageLoad() {
  imageLoading = false
  elements.imageLoader.classList.add("hidden")
  elements.slideImg.style.opacity = "1"
}

function handleImageError() {
  imageLoading = false
  elements.imageLoader.classList.add("hidden")
  showError("Failed to load image")
}

function setupImage(imageSrc) {
  imageLoading = true
  elements.imageLoader.classList.remove("hidden")
  elements.slideImg.style.opacity = "0.5"

  elements.slideImg.onload = handleImageLoad
  elements.slideImg.onerror = handleImageError
  elements.slideImg.src = imageSrc
}

// Main functionality
async function startGeneration() {
  const duration = Number.parseInt(elements.duration.value) || 15
  tuneDuration = duration // Store the user-selected duration

  try {
    showLoading(true, "Selecting images and starting generation...")

    const response = await fetch("/start", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ duration }),
    })

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`)
    }

    const result = await response.json()

    if (result.status === "error") {
      throw new Error(result.message)
    }

    isRunning = true
    totalImages = result.selected_count || 10
    generationComplete = false
    updateButtonStates()
    elements.welcomeMessage.classList.add("hidden")

    // Start polling for updates
    intervalId = setInterval(updateStatus, 1000)

    showLoading(true, `Generating tunes for ${totalImages} selected images...`)
  } catch (error) {
    console.error("Start error:", error)
    showError("Failed to start generation. Please check server connection.")
    showLoading(false)
  }
}

async function stopGeneration() {
  try {
    const response = await fetch("/stop", { method: "POST" })

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`)
    }

    isRunning = false
    generationComplete = false
    totalImages = 0
    updateButtonStates()

    if (intervalId) {
      clearInterval(intervalId)
      intervalId = null
    }

    // Fade out current audio before stopping
    if (currentAudio && isPlaying) {
      await fadeOut(currentAudio, 500)
    }

    cleanupAudio()
    elements.mainContent.classList.add("hidden")
    elements.welcomeMessage.classList.remove("hidden")
    showLoading(false)

    // Reset file tracking
    currentImageFile = null
    currentTuneFile = null

    // Reset stats
    elements.time.textContent = "0s"
    elements.count.textContent = "0"
    elements.remaining.textContent = "—"
  } catch (error) {
    console.error("Stop error:", error)
    showError("Failed to stop generation")
  }
}

async function updateStatus() {
  try {
    const response = await fetch("/status")

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`)
    }

    const data = await response.json()

    // Simplified timing logic - let the audio play naturally
    if (generationComplete && currentAudio && !currentAudio.paused) {
      // During audio playback, show audio time and remaining time
      const audioTime = currentAudio.currentTime || 0
      const audioDuration = currentAudio.duration || 0
      
      elements.time.textContent = formatTime(audioTime)
      elements.remaining.textContent = formatTime(Math.max(0, audioDuration - audioTime))
    } else {
      // During generation or when audio is paused, show server elapsed time
      elements.time.textContent = `${Math.ceil(data.elapsed)}s`
      elements.remaining.textContent = data.remaining ? `${data.remaining}s` : "—"
    }

    // Update count
    elements.count.textContent = `${data.count}/${data.total_images || totalImages}`

    // Update generation status
    if (data.generation_complete && !generationComplete) {
      generationComplete = true
      showLoading(false)
      showError("🎵 All tunes generated! Starting playback sequence...")
    }

    // Handle synchronized playback during generation complete phase
    if (data.generation_complete && data.image && data.tune) {
      const imageChanged = currentImageFile !== data.image
      const tuneChanged = currentTuneFile !== data.tune

      // Show main content
      elements.mainContent.classList.remove("hidden")
      elements.welcomeMessage.classList.add("hidden")

      // If this is the first image/tune or no audio is currently playing
      if (!currentImageFile || !currentTuneFile || !isPlaying) {
        // Update immediately for the first track or when nothing is playing
        if (imageChanged) {
          currentImageFile = data.image
          const imgSrc = `/image/${data.image}?${Date.now()}`
          setupImage(imgSrc)
        }

        if (tuneChanged) {
          currentTuneFile = data.tune
          const tuneSrc = `/tune/${data.tune}?${Date.now()}`
          await setupAudio(tuneSrc)
        }
      } else if ((imageChanged || tuneChanged) && isPlaying) {
        // If audio is playing and we have new content, wait for current audio to end
        pendingImageFile = data.image
        pendingTuneFile = data.tune
        waitingForAudioEnd = true
        
        console.log("Waiting for current audio to end before switching to next track...")
      }

      // Update sequence info in UI
      if (data.current_index) {
        const sequenceInfo = document.querySelector(".audio-header p")
        if (sequenceInfo) {
          sequenceInfo.textContent = `Track ${data.current_index}/${data.total_images} - Based on image colors and features`
        }
      }
    }

    // Show loading during generation phase
    if (!data.generation_complete && isRunning) {
      showLoading(true, `Generating tunes... (${data.count}/${data.total_images || totalImages} complete)`)
    }
  } catch (error) {
    console.error("Status update error:", error)
    showError("Connection lost. Please check if server is running.")

    // Stop polling on persistent errors
    if (intervalId) {
      clearInterval(intervalId)
      intervalId = null
    }
    isRunning = false
    generationComplete = false
    updateButtonStates()
    showLoading(false)
  }
}

async function togglePlayPause() {
  if (!currentAudio || audioLoading || isTransitioning) return

  if (isPlaying) {
    await fadeOut(currentAudio, 300)
  } else {
    await fadeIn(currentAudio, 300)
  }
}

// Event listeners
elements.startBtn.addEventListener("click", startGeneration)
elements.stopBtn.addEventListener("click", stopGeneration)
elements.playPauseBtn.addEventListener("click", togglePlayPause)
elements.closeError.addEventListener("click", () => {
  elements.errorToast.classList.add("hidden")
})

// Keyboard shortcuts
document.addEventListener("keydown", (event) => {
  if (event.code === "Space" && currentAudio && !audioLoading && !isTransitioning) {
    event.preventDefault()
    togglePlayPause()
  }

  if (event.code === "Escape") {
    elements.errorToast.classList.add("hidden")
  }
})

// Cleanup on page unload
window.addEventListener("beforeunload", () => {
  if (intervalId) {
    clearInterval(intervalId)
  }
  cleanupAudio()
})

// Initialize
updateButtonStates()

// Declare event handlers for audio
function handleAudioLoadStart() {}
function handleAudioCanPlay() {}
function handleAudioLoadedMetadata() {}
function handleAudioError() {}

