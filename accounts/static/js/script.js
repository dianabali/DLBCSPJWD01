const main = document.querySelector('main'); // Main container for speech boxes
const voicesSelect = document.getElementById('voices'); // Dropdown for selecting voices
const textarea = document.getElementById('text'); // Textarea for custom text input
const readBtn = document.getElementById('read'); // Button to read the text
const toggleBtn = document.getElementById('toggle'); // Button to toggle the text box visibility
const closeBtn = document.getElementById('close'); // Button to close the text box

// Speech cards: image + text
const data = [
    {
        image: 'drink.png',
        text: "I'm thirsty"
    },
    {
        image: 'food.png',
        text: "I'm hungry"
    },
    {
        image: 'happy.png',
        text: "I'm happy"
    },
    {
        image: 'sad.png',
        text: "I'm sad"
    },
    {
        image: 'angry.png',
        text: "I'm angry"
    },
    {
        image: 'tired.png',
        text: "I'm tired"
    },
    {
        image: 'hurt.png',
        text: "I'm hurt"
    },
    {
        image: 'scared.png',
        text: "I'm scared"
    },
    {
        image: 'home.png',
        text: "I want to go home"
    },
    {
        image: 'school.png',
        text: "I want to go to school"
    },
    {
        image: 'play.png',
        text: "Let's play together"
    },
    {
        image: 'heart.png',
        text: "I love you"
    }
];

data.forEach(createBox);

// Create speech boxes
function createBox(item) {
    const box = document.createElement('div');
    const { image, text } = item;
    
    // Use the current theme if defined, otherwise default to 'blue'
    box.classList.add('box');
    box.innerHTML = `
        <img src="/static/img/${currentTheme}/${image}" alt="${text}" />
        <p class="info">${text}</p>
    `;

    main.appendChild(box);
}


//Init speech synthesis
const message = new SpeechSynthesisUtterance();

// Store voices
let voices = [];

// Get voices from speech synthesis
function getVoices() {
    voices = speechSynthesis.getVoices();

    // Clear the dropdown first
    voicesSelect.innerHTML = '';

    // Populate the dropdown with available voices
    voices.forEach(voice => {
        const option = document.createElement('option');
        option.value = voice.name;
        option.innerText = `${voice.name} (${voice.lang})`;
        voicesSelect.appendChild(option);
    });

    // Only set default voice if none is set yet
    if (!message.voice && voices.length > 0) {
        message.voice = voices[0]; // Set the first available voice as default
        voicesSelect.value = voices[0].name;
    }
}

// Set text message
function setTextMessage(text) {
    message.text = text;
}

// Speak text
function speakText() {
    speechSynthesis.speak(message);
}

// Set voice
function setVoice(e) {
    message.voice = voices.find(voice => voice.name === e.target.value);
}

// Voices changed
speechSynthesis.addEventListener('voiceschanged', getVoices);

// Toggle text box
toggleBtn.addEventListener('click', () => document.getElementById('text-box').classList.toggle('show'));

// Close button
closeBtn.addEventListener('click', () => document.getElementById('text-box').classList.remove('show'));

// Change voice
voicesSelect.addEventListener('change', setVoice);

// Read text button
readBtn.addEventListener('click', () => {
    setTextMessage(textarea.value);
    speakText();
});

// Initialize voices on page load
getVoices();

// Add click event to each box
document.querySelectorAll('main .box').forEach(box => {
    box.addEventListener('click', (e) => {
        
        // Check if the click was on a delete button 
        if (e.target.closest('.delete-btn') || e.target.closest('.delete-form')) {
            e.stopPropagation();
            return; // Don't trigger speech
        }

        // If the click was on the box, get the text and speak it
        const text = box.querySelector('.info').innerText;
        console.log('Box clicked:', text);
        setTextMessage(text);
        speakText();

        // Add active class for animation
        box.classList.add('active');
        setTimeout(() => box.classList.remove('active'), 800);
    });
});


const theme = (typeof currentTheme !== 'undefined') ? currentTheme : 'blue'; // Use current theme if defined, otherwise default to 'blue'
const imagePath = `static/img/${theme}/${image}`; // Update image paths in boxes