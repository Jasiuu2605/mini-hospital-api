document.querySelectorAll('.approve-btn').forEach((button) => {
    button.addEventListener('click', async () => {
        const requestId = button.dataset.requestId;

        const response = await fetch(
            `/requests/${requestId}/status?status=approved`,
            { method: "PATCH" }
        );

        if (!response.ok) {
            alert("Nie udało się zatwierdzić zapotrzebowania.");
            return;
        }

        const statusBadge = button.closest("td").querySelector(".status");

        statusBadge.textContent = "Zatwierdzone";
        statusBadge.classList.remove("pending");
        statusBadge.classList.add("approved");

        button.remove()
    })
})