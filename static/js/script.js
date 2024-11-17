document.addEventListener('DOMContentLoaded', () => {
    // Confirmation dialog for removing a topic
    const removeButtons = document.querySelectorAll('.btn-danger');
    removeButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const topic = e.target.closest('li').textContent.trim();
            const confirmed = confirm(`Are you sure you want to remove the topic: "${topic}"?`);
            if (!confirmed) {
                e.preventDefault(); // Prevent navigation if not confirmed
            }
        });
    });

    // Auto-hide success/danger alerts after 3 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.display = 'none';
        }, 3000);
    });
});
