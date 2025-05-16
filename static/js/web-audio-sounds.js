/**
 * Web Audio API Sound System for Gomoku Master
 * Implements sound effects using the Web Audio API for better performance and control
 */

// Audio Context
let audioContext;

/**
 * Initialize the Web Audio API
 * Sets up the audio context and handles browser compatibility
 */
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

/**
 * Enhanced stone placement sound with resonance
 * Creates a more realistic stone placement sound
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

/**
 * Check for browser support and provide fallbacks
 */
function initSoundSystem() {
    // Primary check for Web Audio API support
    const hasWebAudio = 'AudioContext' in window || 'webkitAudioContext' in window;
    
    if (hasWebAudio) {
        initAudio();  // Initialize audio context
    } else {
        // Fallback for browsers without Web Audio API support
        console.warn('Web Audio API not supported - using silent mode');
        
        // Create silent versions of all sound functions
        window.playStoneSound = function() { console.log('Stone sound (silent mode)'); };
        window.playWinSound = function() { console.log('Win sound (silent mode)'); };
        window.playDrawSound = function() { console.log('Draw sound (silent mode)'); };
        window.playErrorSound = function() { console.log('Error sound (silent mode)'); };
        window.playEnhancedStoneSound = function() { console.log('Enhanced stone sound (silent mode)'); };
    }
    
    // Handle browsers that require user interaction to start audio
    document.addEventListener('click', function audioUnlock() {
        if (audioContext && audioContext.state === 'suspended') {
            audioContext.resume();
        }
        document.removeEventListener('click', audioUnlock);
    }, { once: true });
}

// Initialize the sound system when the script loads
document.addEventListener('DOMContentLoaded', initSoundSystem);

// Export sound functions
export {
    initSoundSystem,
    playStoneSound,
    playEnhancedStoneSound,
    playWinSound,
    playDrawSound,
    playErrorSound
};
