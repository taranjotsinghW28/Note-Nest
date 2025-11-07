// static/note.js

// --- Color and Placement Setup ---
const FUN_COLORS = [
    '#D8BFD8', // Lavender
    '#FAFAD2', // Soft Yellow
    '#FFA07A', // Light Coral
    '#ADD8E6'  // Light Sky Blue
];

// These classes apply the TILT via CSS keyframes now
const CORNER_CLASSES = [
    'corner-top-left', 
    'corner-top-right',
    'corner-bottom-left', 
    'corner-bottom-right' 
];

/**
 * Applies a random background color, a random corner class (for tilt), and 
 * the staggered animation delays to every note box on the home page.
 */
function initializeNoteStyles() {
    const notes = document.querySelectorAll('.note-box'); 
    notes.forEach((note, index) => { 
        
        // 1. Random Color Logic
        const colorIndex = Math.floor(Math.random() * FUN_COLORS.length);
        note.style.backgroundColor = FUN_COLORS[colorIndex];

        // 2. Random Placement/Tilt Logic
        const cornerIndex = Math.floor(Math.random() * CORNER_CLASSES.length);
        const selectedCorner = CORNER_CLASSES[cornerIndex];
        
        // Apply the base corner class.
        note.classList.add(selectedCorner);
        
        // 3. Staggered Entrance Animation Delay (for noteSwing)
        const baseDelay = index * 0.1; 
        const randomExtraDelay = Math.random() * 0.2; 
        const totalEntranceDelay = baseDelay + randomExtraDelay;
        
        // Apply the delay for the initial swing animation
        note.style.animationDelay = `${totalEntranceDelay}s`;

        // 4. Floating Effect Delay: Start the floating animation after the swing finishes
        const ANIMATION_DURATION = 2.2; 
        const FLOAT_START_DELAY = ANIMATION_DURATION + 0.3 + totalEntranceDelay; 
        
        setTimeout(() => {
            // Add the 'floating' class to start the float-with-tilt animation
            note.classList.add('floating'); 
        }, FLOAT_START_DELAY * 1000); // Convert seconds to milliseconds
    });
}

/**
 * Fixes the CSS conflict: Stops the continuous floating animation on hover 
 * and resumes it on mouse leave.
 */
function initializeHoverFix() {
    const notes = document.querySelectorAll('.note-box');
    
    notes.forEach(note => {
        // Mouse Enter: PAUSE the continuous floating animation
        note.addEventListener('mouseenter', () => {
            note.classList.remove('floating');
        });
        
        // Mouse Leave: RESUME the continuous floating animation
        note.addEventListener('mouseleave', () => {
            note.classList.add('floating');
        });
    });
}

/**
 * Applies a subtle scale/shadow effect when an authentication input field is focused.
 */
function initializeInputFocusPop() {
    // Select all inputs inside the main forms for consistency
    const inputs = document.querySelectorAll('.signin-box input, .signup input');

    inputs.forEach(input => {
        // Apply 'input-focus-pop' class when field gets focus
        input.addEventListener('focus', () => {
            input.classList.add('input-focus-pop');
        });

        // Remove class when focus is lost
        input.addEventListener('blur', () => {
            input.classList.remove('input-focus-pop');
        });
    });
}


// ----------------------------------------------------
// --- Core DOM Loading and Event Handlers ---
// ----------------------------------------------------

document.addEventListener("DOMContentLoaded", () => {
    // 🌟 INITIALIZATION FUNCTIONS 🌟
    initializeNoteStyles(); 
    initializeHoverFix(); 
    initializeInputFocusPop(); // 🌟 NEW CALL FOR FORM ANIMATION 🌟
    
    const container = document.querySelector(".notes-container");
    if (!container) {
        console.warn("note.js: .notes-container not found on page.");
        return;
    }

    // Delegated click handler: catches clicks on any .note-box or inside it
    container.addEventListener("click", (e) => {
        const box = e.target.closest(".note-box");
        if (!box) return; 

        // Ignore clicks on interactive elements inside the card (links, buttons, forms, inputs)
        if (e.target.closest("a") || e.target.closest("button") || e.target.closest("form") || e.target.closest("input") || e.target.closest("textarea")) {
            console.log("note.js: click inside control — not toggling. target:", e.target.tagName);
            return;
        }

        // Toggle expanded on the clicked note and collapse others
        const allBoxes = container.querySelectorAll(".note-box");
        allBoxes.forEach(b => {
            if (b === box) {
                b.classList.toggle("expanded");
                console.log("note.js:", b.classList.contains("expanded") ? "expanded" : "collapsed", "note-id:", b.dataset.noteId);
            } else {
                b.classList.remove("expanded");
            }
        });
    });

    // Tag form toggler used by inline onclick="toggleTagForm(id)"
    window.toggleTagForm = function(noteId) {
        const form = document.getElementById("tag-form-" + noteId);
        if (!form) {
            console.warn("toggleTagForm: form not found for", noteId);
            return;
        }
        form.classList.toggle("active");
        if (form.classList.contains("active")) {
            const input = form.querySelector('input[name="tag_name"]');
            if (input) input.focus();
        }
    };

    // Close tag forms when clicking outside
    document.addEventListener("click", (ev) => {
        if (ev.target.closest(".addtag-btn") || ev.target.closest(".tag-form")) return;
        document.querySelectorAll(".tag-form.active").forEach(f => f.classList.remove("active"));
    });

    console.log("note.js loaded — delegation attached on .notes-container");
});


// Tilt effect for Add/Update Note containers (Includes Auth Boxes)
document.addEventListener("DOMContentLoaded", () => {
    // 🌟 Updated selector to include sign-in/up boxes for the tilt effect 🌟
    const tiltBoxes = document.querySelectorAll(
        ".add-note-container, .update-note-container, .signin-box, .signup form"
    );
    tiltBoxes.forEach(box => {
        box.addEventListener("mousemove", (e) => {
            const rect = box.getBoundingClientRect();
            const x = e.clientX - rect.left; 
            const y = e.clientY - rect.top;  
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = ((y - centerY) / centerY) * 6; 
            const rotateY = ((x - centerX) / centerX) * 6;

            box.style.transform = `perspective(900px) rotateX(${-rotateX}deg) rotateY(${rotateY}deg) translateY(-6px) scale(1.01)`;
        });

        box.addEventListener("mouseleave", () => {
            box.style.transform = "perspective(900px) rotateX(0deg) rotateY(0deg) translateY(0) scale(1)";
        });
    });
});