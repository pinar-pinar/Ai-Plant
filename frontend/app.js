async function postImage(file) {
  const fd = new FormData();
  fd.append('file', file);
  const res = await fetch('/api/diagnose/image', { method: 'POST', body: fd });
  return res.json();
}

async function postSymptoms(text) {
  const fd = new FormData();
  fd.append('symptoms', text);
  const res = await fetch('/api/diagnose/symptoms', { method: 'POST', body: fd });
  return res.json();
}

async function chat(msg) {
  const res = await fetch('/api/chat', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({message: msg}) });
  return res.json();
}

document.getElementById('imageForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const file = document.getElementById('imageInput').files[0];
  if(!file) return;
  document.getElementById('imageResult').textContent = 'Envoi...';
  const r = await postImage(file);
  document.getElementById('imageResult').textContent = JSON.stringify(r, null, 2);
});

document.getElementById('symptomForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const txt = document.getElementById('symptoms').value;
  document.getElementById('symptomResult').textContent = 'Analyse...';
  const r = await postSymptoms(txt);
  document.getElementById('symptomResult').textContent = JSON.stringify(r, null, 2);
});

document.getElementById('chatForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const txt = document.getElementById('chatMsg').value;
  document.getElementById('chatResult').textContent = 'Réponse...';
  const r = await chat(txt);
  document.getElementById('chatResult').textContent = JSON.stringify(r, null, 2);
});

async function loadDiseases(){
  const res = await fetch('/api/diseases');
  const data = await res.json();
  const el = document.getElementById('diseasesList');
  el.innerHTML = data.map(d => `<div class=\"disease\"><h3>${d.name}</h3><p>${d.description}</p></div>`).join('\n');
}

loadDiseases();
