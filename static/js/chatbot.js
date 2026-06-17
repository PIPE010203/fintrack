/* ============================================================
   FinTrack — Chatbot: OpenAI-powered financial assistant UI
   ============================================================ */

(function () {
  var csrfMeta = document.querySelector('meta[name="csrf-token"]');
  if (!csrfMeta) return;
  var csrfToken = csrfMeta.getAttribute('content');

  var inputEl = document.getElementById('mensaje-input');
  var chatBox = document.getElementById('chat-box');
  if (!inputEl || !chatBox) return;

  function enviarMensaje() {
    var mensaje = inputEl.value.trim();
    if (!mensaje) return;

    chatBox.innerHTML +=
      '<div class="mb-3 text-end">' +
        '<span class="badge bg-secondary">Tú</span>' +
        '<div class="mt-1 p-2 bg-primary text-white rounded">' + escapeHtml(mensaje) + '</div>' +
      '</div>';

    inputEl.value = '';
    chatBox.scrollTop = chatBox.scrollHeight;

    chatBox.innerHTML +=
      '<div id="typing" class="mb-3">' +
        '<span class="badge bg-primary">FinTrack IA</span>' +
        '<div class="mt-1 p-2 bg-white rounded border text-muted">Escribiendo...</div>' +
      '</div>';
    chatBox.scrollTop = chatBox.scrollHeight;

    fetch('/chatbot/enviar/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({ mensaje: mensaje })
    })
    .then(function (res) { return res.json(); })
    .then(function (data) {
      var typing = document.getElementById('typing');
      if (typing) typing.remove();
      chatBox.innerHTML +=
        '<div class="mb-3">' +
          '<span class="badge bg-primary">FinTrack IA</span>' +
          '<div class="mt-1 p-2 bg-white rounded border">' + escapeHtml(data.respuesta) + '</div>' +
        '</div>';
      chatBox.scrollTop = chatBox.scrollHeight;
    });
  }

  inputEl.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') enviarMensaje();
  });

  var btn = document.querySelector('#enviar-btn');
  if (btn) btn.addEventListener('click', enviarMensaje);

  function escapeHtml(str) {
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }
})();
