// scripts.js

document.addEventListener('DOMContentLoaded', () => {
    // --- Carousel Scrolling Functionality ---
    const videoCarousel = document.getElementById('videoCarousel');
    // NOTE: Changed IDs to be more specific to avoid conflict with future sections
    const videoScrollLeftBtn = document.getElementById('videoScrollLeftBtn');
    const videoScrollRightBtn = document.getElementById('videoScrollRightBtn');

    // Ensure the Editor's Picks IDs are correctly updated in its HTML/JS too
    const editorPicksCarousel = document.getElementById('editorPicksCarousel');
    const editorPicksScrollLeftBtn = document.getElementById('editorPicksScrollLeftBtn');
    const editorPicksScrollRightBtn = document.getElementById('editorPicksScrollRightBtn');


    // Video Carousel Logic
    const videoScrollDistance = 300; 

    const updateVideoCarouselButtonState = () => {
        if (!videoCarousel) return;
        videoScrollLeftBtn.disabled = videoCarousel.scrollLeft <= 0;
        const maxScroll = videoCarousel.scrollWidth - videoCarousel.clientWidth;
        videoScrollRightBtn.disabled = videoCarousel.scrollLeft >= maxScroll - 5; 
    };

    if (videoCarousel) {
        videoScrollRightBtn.addEventListener('click', (e) => {
            e.preventDefault();
            videoCarousel.scrollLeft += videoScrollDistance;
            setTimeout(updateVideoCarouselButtonState, 350); 
        });

        videoScrollLeftBtn.addEventListener('click', (e) => {
            e.preventDefault();
            videoCarousel.scrollLeft -= videoScrollDistance;
            setTimeout(updateVideoCarouselButtonState, 350);
        });

        videoCarousel.addEventListener('scroll', updateVideoCarouselButtonState);
        updateVideoCarouselButtonState();
    }
    
    // Editor's Picks Carousel Logic (Reuse the logic from the previous step)
    // ...

    
    videoCarousel.addEventListener('click', (e) => {
        const videoCard = e.target.closest('.video-card');
        const playButton = e.target.closest('.play-icon');

        if (playButton && videoCard) {
            e.preventDefault();

            // 1. Find elements
            const videoElement = videoCard.querySelector('.f1-video-player');
            const durationTag = videoCard.querySelector('.duration');
            
            // 2. Pause any other playing video
            document.querySelectorAll('.f1-video-player').forEach(vid => {
                if (vid !== videoElement) {
                    vid.pause();
                    // Show play button/duration for other paused videos
                    const otherCard = vid.closest('.video-card');
                    otherCard.querySelector('.play-icon').style.display = 'block';
                    const otherDuration = otherCard.querySelector('.duration');
                    if (otherDuration) otherDuration.style.display = 'block';
                }
            });

            // 3. Load the source URL if it hasn't been set yet
            if (!videoElement.hasAttribute('src')) {
                const videoUrl = videoElement.dataset.videoUrl;
                
                // Set the source and load the video data
                videoElement.setAttribute('src', videoUrl);
                videoElement.load();
               
            }

            // 4. Play the video and hide overlays
            videoElement.play();
            playButton.style.display = 'none';
            if (durationTag) durationTag.style.display = 'none';
            
            // 5. Handle pause/end events
            videoElement.onpause = () => {
                playButton.style.display = 'block';
            };
            videoElement.onplay = () => {
                playButton.style.display = 'none';
            };
            videoElement.onended = () => {
                playButton.style.display = 'block';
                if (durationTag) durationTag.style.display = 'block';
            };
            
            // Optional: Pause/Play if user clicks the video itself
            videoElement.onclick = () => {
                if (videoElement.paused) {
                    videoElement.play();
                } else {
                    videoElement.pause();
                }
            };
        }
    });


});


// drivers and team toggle functionality





document.addEventListener('DOMContentLoaded', () => {
    const toggleButtons = document.querySelectorAll('.toggle-btn');
    const standingsSections = document.querySelectorAll('.standings-section');

    toggleButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetId = button.getAttribute('data-target');

            // --- 1. Manage Button Active State ---
         
            toggleButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            // --- 2. Manage Section Visibility ---
           
            standingsSections.forEach(section => {
                section.classList.add('hidden');
                section.classList.remove('active');
            });

            // Show the target section
            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                targetSection.classList.remove('hidden');
                targetSection.classList.add('active');
            }
        });
    });
});




// news page js

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const filterButtons = document.querySelectorAll('.filter-btn');
    const newsArticles = document.querySelectorAll('.news-article');
    const loadMoreBtn = document.getElementById('load-more-btn');
    
    // Configuration
    const ARTICLES_PER_LOAD = 4; 
    let currentlyVisibleArticles = 0;
    let currentFilter = 'all';


    // Function to handle the visibility of articles based on the current filter
    const updateArticleVisibility = (category) => {
        currentlyVisibleArticles = 0;
        currentFilter = category;

        const filteredArticles = Array.from(newsArticles).filter(article => 
            category === 'all' || article.getAttribute('data-category') === category
        );

        newsArticles.forEach(article => article.classList.add('hidden'));

        filteredArticles.slice(0, ARTICLES_PER_LOAD).forEach(article => {
            article.classList.remove('hidden');
        });
        currentlyVisibleArticles = ARTICLES_PER_LOAD;

        updateLoadMoreButton(filteredArticles.length);
    };

    // Function to handle the Load More button click
    const loadNextBatch = () => {
        const articlesToLoad = Array.from(newsArticles).filter(article => 
            currentFilter === 'all' || article.getAttribute('data-category') === currentFilter
        );

        const nextBatch = articlesToLoad.slice(
            currentlyVisibleArticles, 
            currentlyVisibleArticles + ARTICLES_PER_LOAD
        );

        nextBatch.forEach(article => {
            article.classList.remove('hidden');
        });

        currentlyVisibleArticles += nextBatch.length;

        updateLoadMoreButton(articlesToLoad.length);
    };

    // Function to show/hide the Load More button
    const updateLoadMoreButton = (totalFilteredCount) => {
        if (currentlyVisibleArticles >= totalFilteredCount) {
            loadMoreBtn.classList.add('hidden');
        } else {
            loadMoreBtn.classList.remove('hidden');
        }
    };


    // --- Event Listeners ---

    // 1. Filter Button Click Handler
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            const filterCategory = button.getAttribute('data-category');

            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            updateArticleVisibility(filterCategory);
        });
    });

    loadMoreBtn.addEventListener('click', loadNextBatch);

   
    updateArticleVisibility('all');
});



// Team page load more function
document.addEventListener('DOMContentLoaded', function() {
    const cardsContainer = document.getElementById('teams-grid');
    const loadMoreBtn = document.getElementById('load-more-btn');
    const cards = cardsContainer.querySelectorAll('.team-card');
    const cardsPerLoad = 4;
    let currentVisibleCount = cardsPerLoad;

    /**
     * Hides all cards initially, except for the first 'cardsPerLoad' cards.
     */
    function initializeCards() {
        // 1. Initially hide cards starting from the 5th one (index 4)
        cards.forEach((card, index) => {
            if (index >= cardsPerLoad) {
                card.classList.add('hidden-card');
            }
        });

        // 2. Check if the button is needed
        checkButtonVisibility();
    }

    /**
     * Shows the next batch of cards when the button is clicked.
     */
    function loadMoreCards() {
        const nextBatchEnd = currentVisibleCount + cardsPerLoad;
        
        // Loop through the cards to show the next batch
        for (let i = currentVisibleCount; i < nextBatchEnd; i++) {
            if (cards[i]) {
                cards[i].classList.remove('hidden-card');
            }
        }
        
        // Update the count
        currentVisibleCount = nextBatchEnd;

        // Check if all cards are now visible
        checkButtonVisibility();
    }

    /**
     * Hides the load more button if all cards are visible.
     */
    function checkButtonVisibility() {
        if (currentVisibleCount >= cards.length) {
            loadMoreBtn.style.display = 'none'; // Hide the button
            console.log("All cards loaded.");
        } else {
            loadMoreBtn.style.display = 'block'; // Ensure the button is visible if there are more cards
        }
    }

    // Attach the event listener to the "Load More" button
    loadMoreBtn.addEventListener('click', loadMoreCards);

    // Run the initialization function when the page loads
    initializeCards();
});




// footer dropdown js



        document.addEventListener("DOMContentLoaded", function () {

            const toggleBtn = document.getElementById("userToggle");
            const dropdown = document.getElementById("dropdownMenu");
            const arrow = document.querySelector(".arrow-icon");

            toggleBtn.addEventListener("click", function (e) {
                e.stopPropagation();

                dropdown.classList.toggle("dropdown-show");
                arrow.classList.toggle("arrow-rotate");
            });

            document.addEventListener("click", function () {
                dropdown.classList.remove("dropdown-show");
                arrow.classList.remove("arrow-rotate");
            });

        });

   

    // <!-- cookies js -->
    
        document.addEventListener("DOMContentLoaded", function () {

            const cookiePopup = document.getElementById("cookiePopup");

            // SHOW ONLY FIRST TIME
            if (localStorage.getItem("cookieConsent") === "true") {
                cookiePopup.classList.add("hidden");
            } else {
                cookiePopup.classList.remove("hidden");
            }

            // ACCEPT ALL BUTTON
            document.getElementById("acceptCookies").addEventListener("click", function () {
                localStorage.setItem("cookieConsent", "true");
                cookiePopup.classList.add("hidden");
            });

            // SETTINGS BUTTON
            document.getElementById("manageCookies").addEventListener("click", function () {
                alert("Cookie settings panel coming soon!");
                // Later we can open a real manage panel here
            });

        });
    