async function init() {
  try {
    const res = await fetch('/api/config/public');
    const data = await res.json();
    new QRCode(document.getElementById("qrcode"), { text: `${data.public_url}/participante.html`, width: 120, height: 120 });
  } catch (e) {}
  fetchWords();
  setInterval(fetchWords, 3000);
}
async function fetchWords() {
  try {
    const res = await fetch('/api/cloud/words');
    const data = await res.json();
    document.getElementById('totalCount').innerText = data.total_approved;
  } catch (e) {}
}
window.onload = init;