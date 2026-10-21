// Configuração do QR Code
const currentUrl = window.location.href;
document.getElementById('qrCodeImg').src = 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=' + encodeURIComponent(currentUrl);

const colors = ['#ffd700', '#ff2e63', '#00f5d4', '#ffffff', '#ff75c3', '#ffb6c1'];

// Palavras padrão caso o banco esteja vazio/a carregar
const defaultWords = [
  { word: "NATAL", frequency: 5 },
  { word: "SENAI", frequency: 5 },
  { word: "INOVAÇÃO", frequency: 4 },
  { word: "UNIÃO", frequency: 4 },
  { word: "TECNOLOGIA", frequency: 3 },
  { word: "PAZ", frequency: 3 },
  { word: "ESPERANÇA", frequency: 3 },
  { word: "ALEGRIA", frequency: 2 },
  { word: "AMOR", frequency: 2 },
  { word: "FUTURO", frequency: 2 },
  { word: "SAÚDE", frequency: 1 },
  { word: "FESTA", frequency: 1 }
];

function renderTree(words) {
  const container = document.getElementById('treeCloud');
  container.innerHTML = '';

  const rows = [
    document.createElement('div'),
    document.createElement('div'),
    document.createElement('div'),
    document.createElement('div'),
    document.createElement('div')
  ];

  rows.forEach(r => { 
    r.className = 'tree-row'; 
    container.appendChild(r); 
  });

  words.forEach((item, index) => {
    const span = document.createElement('span');
    span.className = 'word-tag';
    span.innerText = item.word;
    
    const fontSize = Math.min(Math.max((item.frequency || 1) * 5 + 14, 14), 32);
    span.style.fontSize = fontSize + 'px';

    const color = colors[index % colors.length];
    span.style.color = color;
    span.style.textShadow = '0 0 10px ' + color;
    span.style.animationDuration = (2.5 + (index % 3) * 0.5) + 's';

    let rowIndex = 0;
    if (index > 0 && index <= 2) rowIndex = 1;
    else if (index > 2 && index <= 5) rowIndex = 2;
    else if (index > 5 && index <= 8) rowIndex = 3;
    else if (index > 8) rowIndex = 4;

    rows[rowIndex].appendChild(span);
  });
}

async function loadWords() {
  try {
    const res = await fetch('/api/words');
    if (res.ok) {
      const data = await res.json();
      if (Array.isArray(data) && data.length > 0) {
        renderTree(data);
        return;
      }
    }
  } catch(e) {}
  renderTree(defaultWords);
}

document.getElementById('wordForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const input = document.getElementById('wordInput');
  const val = input.value.trim();
  if (val) {
    try {
      await fetch('/api/words', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ word: val })
      });
    } catch(e) {}
    input.value = '';
    loadWords();
  }
});

loadWords();