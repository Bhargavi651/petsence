async function sendChat() {
    const input = document.getElementById("chatInput").value;
    const res = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
    });
    const data = await res.json();
    const reply = document.getElementById("chatReply");
    reply.innerText = data.reply;
    reply.classList.remove("hidden");
}

async function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(async (position) => {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;

            const res = await fetch('/nearby', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ lat, lng, type: 'veterinary_care' })
            });
            const data = await res.json();
            const results = document.getElementById("clinicResults");
            results.innerHTML = '';

            data.forEach(clinic => {
                results.innerHTML += `<div class="p-3 bg-white shadow rounded">
                    <strong>${clinic.name}</strong><br>
                    ${clinic.vicinity}
                </div>`;
            });
        });
    } else {
        alert("Geolocation is not supported.");
    }
}
