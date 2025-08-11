const form = document.getElementById('search-form');
const resultDiv = document.getElementById('result');
const messageDiv = document.getElementById('message');

function showError(msg) {
  messageDiv.style.display = 'block';
  messageDiv.textContent = msg;
  resultDiv.style.display = 'none';
}

function showResult(data) {
  messageDiv.style.display = 'none';
  resultDiv.style.display = 'block';
  resultDiv.innerHTML = `
    <div><strong>שם המלון:</strong> ${data.hotel_name}</div>
    <div><strong>יעד:</strong> ${data.city} (${data.region})</div>
    <div><strong>מחיר ללילה:</strong> ${data.price_per_night.toFixed(2)} ₪</div>
    <div><strong>מספר לילות:</strong> ${data.nights}</div>
    <div><strong>מחיר כולל:</strong> ${data.total_price.toFixed(2)} ₪</div>
  `;
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const destination = document.getElementById('destination').value.trim();
  const check_in = document.getElementById('check_in').value;
  const check_out = document.getElementById('check_out').value;

  if (!destination || !check_in || !check_out) {
    showError('אנא מלאו את כל השדות');
    return;
  }

  try {
    const res = await fetch('/api/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ destination, check_in, check_out })
    });

    const data = await res.json();
    if (!res.ok) {
      showError(data.detail || 'שגיאה בבקשה');
      return;
    }
    showResult(data);
  } catch (err) {
    showError('שגיאת רשת, נסו שוב.');
  }
});