# Implementing Game Sound Effects with Web Audio API

This guide provides a detailed explanation of how to implement sound effects in web games using the Web Audio API, with specific examples from the Gomoku Master project.

## Table of Contents

1. [Introduction to Web Audio API](#introduction-to-web-audio-api)
2. [Setting Up the Audio Context](#setting-up-the-audio-context)
3. [Sound Effect Implementation](#sound-effect-implementation)
   - [Stone Placement Sound](#stone-placement-sound)
   - [Win Sound](#win-sound)
   - [Draw Sound](#draw-sound)
   - [Error Sound](#error-sound)
4. [Integration with Game Events](#integration-with-game-events)
5. [Browser Compatibility and Fallbacks](#browser-compatibility-and-fallbacks)
6. [Advanced Techniques](#advanced-techniques)

## Introduction to Web Audio API

The Web Audio API is a powerful JavaScript API for creating and manipulating audio directly in the browser. Unlike traditional HTML5 audio elements, it allows for precise control over sound generation, timing, and processing without requiring external audio files.

**Key Benefits:**
- No external audio file dependencies
- Reduced loading times and bandwidth usage
- Programmatic control over sound characteristics
- Cross-browser compatibility
- Low latency audio processing

## Setting Up the Audio Context

The first step in using the Web Audio API is to create an `AudioContext`, which serves as the foundation for all audio operations.

```javascript
// Initialize Web Audio API
let audioContext;

function initAudio() {
    try {
        // Handle browser prefixes for maximum compatibility
        window.AudioContext = window.AudioContext || window.webkitAudioContext;
        audioContext = new AudioContext();
        
        // Some browsers (like Safari) require user interaction before allowing audio
        if (audioContext.state === 'suspended') {
            const resumeAudio = function() {
                audioContext.resume();
                document.body.removeEventListener('click', resumeAudio);
                document.body.removeEventListener('touchstart', resumeAudio);
            };
            document.body.addEventListener('click', resumeAudio);
            document.body.addEventListener('touchstart', resumeAudio);
        }
        
        console.log('Audio context initialized successfully');
    } catch (e) {
        console.warn('Web Audio API is not supported in this browser:', e);
    }
}

// Call this function when the page loads
window.addEventListener('load', initAudio);
```

This code:
1. Creates a cross-browser compatible AudioContext
2. Handles the "suspended" state that occurs in some browsers until user interaction
3. Provides fallback messaging if the Web Audio API isn't supported

## Sound Effect Implementation

### Stone Placement Sound

The stone placement sound provides tactile feedback when a player places a stone on the board. It's a short, subtle "click" sound.

```javascript
/**
 * Plays a sound when a stone is placed on the board
 * Creates a short "click" sound using a sine wave oscillator
 */
function playStoneSound() {
    if (!audioContext) return;
    
    try {
        // Create an oscillator (sound generator)
        const oscillator = audioContext.createOscillator();
        
        // Create a gain node (volume controller)
        const gainNode = audioContext.createGain();
        
        // Configure the oscillator
        oscillator.type = 'sine';  // Sine wave creates a smooth tone
        
        // Start at 500Hz and drop to 300Hz for a "click" effect
        oscillator.frequency.setValueAtTime(500, audioContext.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(300, audioContext.currentTime + 0.2);
        
        // Configure the gain node for volume envelope
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);  // Start at 30% volume
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2);  // Fade out
        
        // Connect the nodes: oscillator -> gain -> speakers
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        // Play the sound
        oscillator.start();  // Start immediately
        oscillator.stop(audioContext.currentTime + 0.2);  // Stop after 0.2 seconds
    } catch (e) {
        console.warn('Error playing stone sound:', e);
    }
}
```

**Key Techniques:**
- **Oscillator Type**: 'sine' creates a smooth, pure tone
- **Frequency Modulation**: Changing from 500Hz to 300Hz creates the "click" effect
- **Gain Envelope**: Starting at 0.3 and fading to 0.01 creates a natural decay
- **Precise Timing**: The sound plays for exactly 0.2 seconds

### Win Sound

The win sound is a celebratory ascending arpeggio that plays when a player wins the game.

```javascript
/**
 * Plays a victory sound when a player wins
 * Creates an ascending arpeggio using musical notes
 */
function playWinSound() {
    if (!audioContext) return;
    
    try {
        // Define musical notes for a C major arpeggio (C5, E5, G5, C6)
        const notes = [523.25, 659.25, 783.99, 1046.50];
        const noteDuration = 0.15;  // Each note plays for 0.15 seconds
        
        // Play each note in sequence
        notes.forEach((frequency, index) => {
            // Create oscillator and gain node for each note
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            // Configure oscillator
            oscillator.type = 'sine';
            oscillator.frequency.value = frequency;
            
            // Configure gain envelope
            // Start at 30% volume and fade out
            gainNode.gain.setValueAtTime(0.3, audioContext.currentTime + index * noteDuration);
            gainNode.gain.exponentialRampToValueAtTime(
                0.01, 
                audioContext.currentTime + (index + 1) * noteDuration
            );
            
            // Connect nodes
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            // Schedule playback
            // Each note starts after the previous one
            oscillator.start(audioContext.currentTime + index * noteDuration);
            oscillator.stop(audioContext.currentTime + (index + 1) * noteDuration);
        });
    } catch (e) {
        console.warn('Error playing win sound:', e);
    }
}
```

**Key Techniques:**
- **Musical Notes**: Using specific frequencies for C5, E5, G5, C6 creates a recognizable melody
- **Sequential Scheduling**: Each note is scheduled to play after the previous one
- **Individual Gain Nodes**: Each note has its own volume envelope
- **Precise Timing**: Notes are spaced exactly 0.15 seconds apart

### Draw Sound

The draw sound indicates when the game ends in a tie, with a descending tone that signals conclusion without victory.

```javascript
/**
 * Plays a sound when the game ends in a draw
 * Creates a descending tone to signal neutral conclusion
 */
function playDrawSound() {
    if (!audioContext) return;
    
    try {
        // Create audio nodes
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        // Configure oscillator
        oscillator.type = 'sine';
        
        // Start at A4 (440Hz) and descend to A3 (220Hz)
        oscillator.frequency.setValueAtTime(440, audioContext.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(220, audioContext.currentTime + 0.5);
        
        // Configure gain envelope
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
        
        // Connect nodes
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        // Play the sound
        oscillator.start();
        oscillator.stop(audioContext.currentTime + 0.5);  // Longer duration (0.5s)
    } catch (e) {
        console.warn('Error playing draw sound:', e);
    }
}
```

**Key Techniques:**
- **Longer Duration**: 0.5 seconds gives a more definitive conclusion
- **Octave Drop**: From 440Hz to 220Hz (one octave) creates a recognizable "game over" feel
- **Smooth Transition**: Using exponentialRampToValueAtTime creates a natural-sounding descent

### Error Sound

The error sound provides immediate feedback when a player attempts an invalid move.

```javascript
/**
 * Plays a sound when an invalid move is attempted
 * Creates a short "buzz" sound to indicate error
 */
function playErrorSound() {
    if (!audioContext) return;
    
    try {
        // Create audio nodes
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        // Configure oscillator
        // Square wave creates a buzzy, electronic sound
        oscillator.type = 'square';
        oscillator.frequency.setValueAtTime(150, audioContext.currentTime);  // Low frequency
        
        // Configure gain envelope
        gainNode.gain.setValueAtTime(0.2, audioContext.currentTime);  // Lower volume (20%)
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2);
        
        // Connect nodes
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        // Play the sound
        oscillator.start();
        oscillator.stop(audioContext.currentTime + 0.2);
    } catch (e) {
        console.warn('Error playing error sound:', e);
    }
}
```

**Key Techniques:**
- **Square Wave**: Creates a harsh, buzzy tone that clearly indicates an error
- **Low Frequency**: 150Hz gives a deep, warning-like sound
- **Lower Volume**: 0.2 (20%) is quieter than other sounds to avoid being too jarring
- **Short Duration**: 0.2 seconds is just long enough to notice without being annoying

## Integration with Game Events

To integrate these sounds with game events, call the appropriate sound function when specific actions occur:

```javascript
// Example: Handling board click
function handleBoardClick(event) {
    if (!gameState.gameActive || gameState.winner) return;
    
    // Get click coordinates and convert to board position
    // ... (coordinate calculation code) ...
    
    // Check if the move is valid
    if (gameState.board[row][col] !== 0) {
        playErrorSound();  // Play error sound for invalid move
        return;
    }
    
    // Make the move
    makeMove(row, col);
}

// Example: Making a move
function makeMove(row, col) {
    // Update board state
    gameState.board[row][col] = gameState.currentPlayer;
    
    // Draw stone and play sound
    drawStone(row, col, gameState.currentPlayer);
    playStoneSound();  // Play stone placement sound
    
    // Check for win
    if (checkWin(row, col)) {
        gameState.winner = gameState.currentPlayer;
        gameState.gameActive = false;
        updateGameStatus();
        playWinSound();  // Play win sound
        return;
    }
    
    // Check for draw
    if (checkDraw()) {
        gameState.gameActive = false;
        updateGameStatus();
        playDrawSound();  // Play draw sound
        return;
    }
    
    // Switch player
    // ... (remaining game logic) ...
}
```

## Browser Compatibility and Fallbacks

To ensure your sound effects work across different browsers:

```javascript
// Check for browser support and provide fallbacks
function initSoundSystem() {
    // Primary check for Web Audio API support
    const hasWebAudio = 'AudioContext' in window || 'webkitAudioContext' in window;
    
    if (hasWebAudio) {
        initAudio();  // Initialize audio context
    } else {
        // Fallback for browsers without Web Audio API support
        console.warn('Web Audio API not supported - using silent mode');
        
        // Create silent versions of all sound functions
        window.playStoneSound = function() {};
        window.playWinSound = function() {};
        window.playDrawSound = function() {};
        window.playErrorSound = function() {};
    }
    
    // Handle browsers that require user interaction to start audio
    document.addEventListener('click', function audioUnlock() {
        if (audioContext && audioContext.state === 'suspended') {
            audioContext.resume();
        }
        document.removeEventListener('click', audioUnlock);
    }, { once: true });
}
```

## Advanced Techniques

For more sophisticated sound effects, you can extend the basic techniques:

```javascript
/**
 * Creates a more realistic stone placement sound with resonance
 */
function playEnhancedStoneSound() {
    if (!audioContext) return;
    
    try {
        // Create nodes
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        const filter = audioContext.createBiquadFilter();
        
        // Configure oscillator
        oscillator.type = 'triangle';  // Triangle wave for more harmonics
        oscillator.frequency.setValueAtTime(600, audioContext.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(300, audioContext.currentTime + 0.15);
        
        // Configure filter for resonance
        filter.type = 'lowpass';
        filter.frequency.value = 1000;
        filter.Q.value = 8;  // Resonance factor
        
        // Configure gain envelope
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
        
        // Connect nodes: oscillator -> filter -> gain -> speakers
        oscillator.connect(filter);
        filter.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        // Play the sound
        oscillator.start();
        oscillator.stop(audioContext.currentTime + 0.3);
    } catch (e) {
        console.warn('Error playing enhanced stone sound:', e);
    }
}
```

This enhanced version adds:
- A triangle wave for richer harmonics
- A resonant filter to simulate the wooden board resonance
- A longer decay for more natural sound

---

By implementing these sound effects using the Web Audio API, you create a more immersive gaming experience without relying on external audio files. This approach ensures your game is truly standalone while providing rich audio feedback that enhances player engagement.
