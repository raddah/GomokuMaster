// Sound files for stone placement
const placeStoneSound = new Audio('./static/sounds/stone_place.mp3');
const winSound = new Audio('./static/sounds/win.mp3');
const drawSound = new Audio('./static/sounds/draw.mp3');
const errorSound = new Audio('./static/sounds/error.mp3');

// Function to play sounds with error handling
function playSound(sound) {
  sound.play().catch(error => {
    console.log("Sound playback error:", error);
  });
}

// Function to initialize all sounds (preload)
function initSounds() {
  // Set volume levels
  placeStoneSound.volume = 0.7;
  winSound.volume = 0.8;
  drawSound.volume = 0.7;
  errorSound.volume = 0.5;
  
  // Preload sounds
  placeStoneSound.load();
  winSound.load();
  drawSound.load();
  errorSound.load();
}

// Export sound functions
export {
  initSounds,
  playSound,
  placeStoneSound,
  winSound,
  drawSound,
  errorSound
};
