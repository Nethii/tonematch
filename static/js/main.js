// static/js/main.js

const uploadArea = document.getElementById('uploadArea');
const imageInput = document.getElementById('imageInput');
const previewImage = document.getElementById('previewImage');
const uploadPlaceholder = document.getElementById('uploadPlaceholder');
const analyseBtn = document.getElementById('analyseBtn');
const loading = document.getElementById('loading');
const errorCard = document.getElementById('errorCard');
const errorMessage = document.getElementById('errorMessage');
const errorDismiss = document.getElementById('errorDismiss');
const resultsSection = document.getElementById('resultsSection');
const tryAgainBtn = document.getElementById('tryAgainBtn');
const fileInfo = document.getElementById('fileInfo');
const noFileInfo = document.getElementById('noFileInfo');
const fileName = document.getElementById('fileName');

let selectedFile = null;

uploadArea.addEventListener('click', () => imageInput.click());

imageInput.addEventListener('change', (e) => {
    if (e.target.files[0]) handleFile(e.target.files[0]);
});

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
});

function handleFile(file) {
    selectedFile = file;
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        previewImage.style.display = 'block';
        uploadPlaceholder.style.display = 'none';
        uploadArea.style.minHeight = '280px';
        uploadArea.style.padding = '0';
    };
    reader.readAsDataURL(file);

    if (fileInfo) { fileInfo.style.display = 'flex'; }
    if (fileName) { fileName.textContent = file.name; }
    if (noFileInfo) { noFileInfo.style.display = 'none'; }
    analyseBtn.disabled = false;
}

analyseBtn.addEventListener('click', async () => {
    if (!selectedFile) return;

    loading.style.display = 'flex';
    errorCard.style.display = 'none';
    resultsSection.style.display = 'none';
    analyseBtn.disabled = true;

    animateLoadingSteps();

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
        const response = await fetch('/analyse', { method: 'POST', body: formData });
        const data = await response.json();
        loading.style.display = 'none';

        if (data.success) {
            showResults(data);
        } else {
            showError(data.error);
        }
    } catch (err) {
        loading.style.display = 'none';
        showError('Something went wrong. Please try again.');
    }
});

function animateLoadingSteps() {
    const steps = ['lstep1', 'lstep2', 'lstep3', 'lstep4'];
    let current = 0;
    steps.forEach(id => {
        const el = document.getElementById(id);
        if (el) { el.classList.remove('active', 'done'); }
    });
    const interval = setInterval(() => {
        if (current > 0) {
            const prev = document.getElementById(steps[current - 1]);
            if (prev) { prev.classList.remove('active'); prev.classList.add('done'); }
        }
        if (current < steps.length) {
            const curr = document.getElementById(steps[current]);
            if (curr) curr.classList.add('active');
            current++;
        } else {
            clearInterval(interval);
        }
    }, 600);
}

// function showResults(data) {
//     document.getElementById('toneSwatch').style.background = data.hex_colour;
//     document.getElementById('skinToneName').textContent = data.skin_tone;
//     document.getElementById('undertoneBadge').textContent = data.undertone + ' Undertone';
//     document.getElementById('undertoneDesc').textContent = data.undertone_description;

//     const makeupGrid = document.getElementById('makeupGrid');
//     makeupGrid.innerHTML = '';
//     for (const [category, colours] of Object.entries(data.makeup)) {
//         const col = document.createElement('div');
//         col.innerHTML = `
//             <p class="makeup-col-title">${category}</p>
//             <ul class="makeup-col-list">
//                 ${colours.map(c => `<li>${c}</li>`).join('')}
//             </ul>
//         `;
//         makeupGrid.appendChild(col);
//     }

//     renderSwatches('clothingSwatches', data.clothing);
//     renderSwatches('hairSwatches', data.hair);

//     resultsSection.style.display = 'block';
//     setTimeout(() => {
//         resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
//     }, 100);
// }

function showResults(data) {
    // Redirect to dedicated results page
    window.location.href = '/results/' + data.result_id;
}

function renderSwatches(containerId, colours) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    colours.forEach(colour => {
        const pill = document.createElement('div');
        pill.className = 'swatch-pill';
        pill.innerHTML = `
            <div class="swatch-dot" style="background:${colourNameToHex(colour)}"></div>
            <span>${colour}</span>
        `;
        container.appendChild(pill);
    });
}

if (tryAgainBtn) {
    tryAgainBtn.addEventListener('click', () => {
        selectedFile = null;
        imageInput.value = '';
        previewImage.style.display = 'none';
        previewImage.src = '';
        uploadPlaceholder.style.display = 'block';
        uploadArea.style.minHeight = '240px';
        uploadArea.style.padding = '';
        analyseBtn.disabled = true;
        resultsSection.style.display = 'none';
        errorCard.style.display = 'none';
        if (fileInfo) fileInfo.style.display = 'none';
        if (noFileInfo) noFileInfo.style.display = 'flex';
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

if (errorDismiss) {
    errorDismiss.addEventListener('click', () => {
        errorCard.style.display = 'none';
        analyseBtn.disabled = false;
    });
}

function showError(message) {
    errorMessage.textContent = message;
    errorCard.style.display = 'block';
    analyseBtn.disabled = false;
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function colourNameToHex(name) {
    const map = {
        'camel':'#C19A6B','terracotta':'#E2725B','warm orange':'#FF8C42',
        'olive':'#808000','mustard yellow':'#FFDB58','rust':'#B7410E',
        'warm brown':'#7B4F2E','navy blue':'#001F5B','royal blue':'#4169E1',
        'emerald':'#50C878','burgundy':'#800020','cool grey':'#9EA3A8',
        'lavender':'#E6E6FA','soft teal':'#7BB8B0','blush pink':'#FFB6C1',
        'sage green':'#B2AC88','dusty blue':'#8FAFC0','warm taupe':'#A08060',
        'soft coral':'#F08070','cream':'#FFFDD0','gold':'#FFD700',
        'bronze':'#CD7F32','copper':'#B87333','cobalt blue':'#0047AB',
        'purple':'#800080','deep teal':'#008080','fuchsia':'#FF00FF',
        'teal':'#008080','forest green':'#228B22','warm white':'#FAF0E6',
        'burnt sienna':'#E97451','dusty rose':'#DCB4B4','orange':'#FFA500',
        'warm red':'#C0392B','yellow':'#FFD700','deep coral':'#FF6B6B',
        'brown':'#A0522D','bright orange':'#FF6600','deep yellow':'#FFC300',
        'olive green':'#6B8E23','royal purple':'#7851A9','bright white':'#FFFFFF',
        'hot pink':'#FF69B4','bright green':'#00CC44','navy':'#001F5B',
        'mauve':'#E0B0C8','silver':'#C0C0C0','champagne':'#F7E7CE',
        'soft pink':'#FFD1DC','wine':'#722F37','plum':'#8E4585',
        'berry':'#8B1A4A','honey blonde':'#F5A623','golden brown':'#996633',
        'caramel brown':'#A0522D','auburn':'#922724','espresso':'#3C1A0E',
        'jet black':'#0A0A0A','natural black':'#1A1A1A','peach':'#FFCBA4',
        'coral':'#FF7F50','warm beige':'#D4B896','natural beige':'#C9A882',
        'sand':'#C2B280','caramel':'#C47A3A','tan':'#D2B48C',
        'ebony':'#3D2314','warm ivory':'#FFF8EE','nude pink':'#D4A5A5',
        'warm rose':'#C96A7A','deep rose':'#C06080','ash brown':'#987654',
        'warm chestnut':'#954535','cool chestnut':'#8B5E3C','dark honey':'#B8860B',
        'light brown':'#A07850','medium brown':'#784030','dark brown':'#5C2E18',
        'soft black':'#1A1010','blue black':'#0A0818','deep burgundy':'#4A0010',
        'warm auburn':'#A52A2A','cool auburn':'#8B3A3A','rich purple':'#6A0DAD',
        'deep gold':'#B8860B','warm navy':'#1A2A5E','warm copper':'#A05030'
    };
    return map[name.toLowerCase()] || generateColour(name);
}

function generateColour(name) {
    let hash = 0;
    for (let i = 0; i < name.length; i++) {
        hash = name.charCodeAt(i) + ((hash << 5) - hash);
    }
    const h = Math.abs(hash) % 60 + 15;
    return `hsl(${h}, 45%, 55%)`;
}