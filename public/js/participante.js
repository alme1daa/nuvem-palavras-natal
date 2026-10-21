document.getElementById('wordForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const input = document.getElementById('wordInput');
  const res = await fetch('/api/submit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ word: input.value })
  });
  if (res.ok) {
    alert('Palavra enviada com sucesso!');
    input.value = '';
  } else {
    alert('Erro ao enviar palavra.');
  }
});