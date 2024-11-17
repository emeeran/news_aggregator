document.addEventListener('DOMContentLoaded', () => {
    // Form handling
    const topicSelect = document.getElementById('topic');
    const customTopicInput = document.getElementById('custom_topic');
    const searchForm = document.querySelector('.search-form');
    const searchButton = document.querySelector('.search-button');

    // Clear custom topic when preset topic is selected
    topicSelect?.addEventListener('change', () => {
        if (topicSelect.value) {
            customTopicInput.value = '';
        }
    });

    // Clear preset topic when custom topic is entered
    customTopicInput?.addEventListener('input', () => {
        if (customTopicInput.value) {
            topicSelect.value = '';
        }
    });

    // Form submission handling
    searchForm?.addEventListener('submit', (e) => {
        if (!topicSelect.value && !customTopicInput.value.trim()) {
            e.preventDefault();
            alert('Please select a topic or enter a custom topic');
            return;
        }

        searchButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
        searchButton.disabled = true;
    });

    // Source filtering
    const filterButtons = document.querySelectorAll('.filter-btn');
    const newsCards = document.querySelectorAll('.news-card');

    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Update active button
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            // Filter news cards
            const source = button.dataset.source;
            newsCards.forEach(card => {
                if (source === 'all') {
                    card.style.display = 'block';
                } else if (source === 'The Hindu') {
                    card.style.display = card.dataset.source === 'hindu' ? 'block' : 'none';
                } else {
                    card.style.display = card.dataset.source === 'general' ? 'block' : 'none';
                }
            });
        });
    });

    // Lazy loading for images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.style.backgroundImage = `url('${img.dataset.src}')`;
                        observer.unobserve(img);
                    }
                }
            });
        });

        document.querySelectorAll('.article-image[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
});