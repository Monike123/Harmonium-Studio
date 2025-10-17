document.getElementById('upload-form').addEventListener('submit', async function (e) {
  e.preventDefault();
  const formData = new FormData(this);

  const response = await fetch('/generate', {
    method: 'POST',
    body: formData
  });

  if (response.ok) {
    const data = await response.json();
    const cacheBuster = `?t=${Date.now()}`;

    const normalUrl = data.normal_url + cacheBuster;
    const enhancedUrl = data.enhanced_url + cacheBuster;

    document.getElementById('output').classList.remove('hidden');
    document.getElementById('raga-info').innerText = `🎼 Raga: ${data.raga}`;
    document.getElementById('swaras-info').innerText = `🎵 Swaras: ${data.swaras.join(', ')}`;

    document.getElementById('audio-source').src = normalUrl;
    document.getElementById('audio-player').load();
    document.getElementById('download-link-normal').href = normalUrl;

    document.getElementById('enhanced-audio-source').src = enhancedUrl;
    document.getElementById('enhanced-audio-player').load();
    document.getElementById('download-link-enhanced').href = enhancedUrl;
  } else {
    alert("Error generating music.");
  }
});
