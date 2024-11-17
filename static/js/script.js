document.addEventListener('DOMContentLoaded', () => {
    const topicSelect = document.getElementById('topic');
    const customTopicInput = document.getElementById('custom_topic');

    // Clear custom topic when preset topic is selected
    topicSelect.addEventListener('change', () => {
        if (topicSelect.value) {
            customTopicInput.value = '';
        }
    });

    // Clear preset topic when custom topic is entered
    customTopicInput.addEventListener('input', () => {
        if (customTopicInput.value) {
            topicSelect.value = '';
        }
    });

    // Add loading state to form submission
    const searchForm = document.querySelector('.search-form');
    const searchButton = document.querySelector('.search-button');

    searchForm.addEventListener('submit', (e) => {
        if (!topicSelect.value && !customTopicInput.value.trim()) {
            e.preventDefault();
            alert('Please select a topic or enter a custom topic');
            return;
        }

        searchButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
        searchButton.disabled = true;
    });

    // Add lazy loading for images
    const lazyLoadImages = () => {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.style.backgroundImage = `url('${img.dataset.src}')`;
                    observer.unobserve(img);
                }
            });
        });

        document.querySelectorAll('.article-image[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    };

    // Initialize lazy loading
    if ('IntersectionObserver' in window) {
        lazyLoadImages();
    }

    // Add smooth scroll to top
    const scrollToTop = () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    };

    // Create scroll to top button
    const scrollButton = document.createElement('button');