/**
 * Table of Contents scroll tracking and navigation.
 *
 * Features:
 * - Highlights the current section in the ToC sidebar
 * - Uses IntersectionObserver for efficient scroll tracking
 * - Smooth scrolling when clicking ToC links
 * - Accounts for sticky header offset
 *
 * @module toc
 */
(function () {
    'use strict';

    /** @const {number} Offset in pixels for sticky header when scrolling */
    const HEADER_OFFSET = 80;

    /** @const {string} Root margin for IntersectionObserver */
    const OBSERVER_ROOT_MARGIN = '-80px 0px -70% 0px';

    /** @type {NodeListOf<HTMLAnchorElement>} All ToC links */
    const tocLinks = document.querySelectorAll('.toc-list a');
    if (!tocLinks.length) return;

    /**
     * Extract heading IDs from ToC links.
     * @type {string[]}
     */
    const headingIds = Array.from(tocLinks)
        .map(function (link) {
            const href = link.getAttribute('href');
            return href ? href.slice(1) : null; // Remove the # prefix
        })
        .filter(Boolean);

    /**
     * Get the actual heading elements from the document.
     * @type {HTMLElement[]}
     */
    const headings = headingIds
        .map(function (id) {
            return document.getElementById(id);
        })
        .filter(Boolean);

    if (!headings.length) return;

    /** @type {string | null} Currently active heading ID */
    let currentActive = null;

    /**
     * Set the active ToC link based on heading ID.
     * Updates the 'active' class on ToC links.
     *
     * @param {string} id - The heading ID to mark as active.
     */
    function setActiveLink(id) {
        if (currentActive === id) return;
        currentActive = id;

        tocLinks.forEach(function (link) {
            const href = link.getAttribute('href');
            if (href === '#' + id) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }

    /**
     * Set the initial active heading based on scroll position.
     * Finds the heading closest to (but above) the current scroll position.
     */
    function setInitialActive() {
        const scrollTop = window.scrollY + 100;

        // Find the heading that's currently at the top (iterate from bottom)
        for (let i = headings.length - 1; i >= 0; i--) {
            if (headings[i].offsetTop <= scrollTop) {
                setActiveLink(headings[i].id);
                return;
            }
        }

        // If no heading is above scroll position, activate first one
        if (headings.length > 0) {
            setActiveLink(headings[0].id);
        }
    }

    /**
     * Scroll to a heading element with smooth animation.
     * Accounts for sticky header offset.
     *
     * @param {HTMLElement} target - The heading element to scroll to.
     */
    function scrollToHeading(target) {
        const elementPosition = target.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.scrollY - HEADER_OFFSET;

        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
    }

    /**
     * Handle click events on ToC links.
     * Prevents default behavior and scrolls smoothly to the heading.
     *
     * @param {MouseEvent} event - The click event.
     * @param {HTMLAnchorElement} link - The clicked link element.
     */
    function handleTocClick(event, link) {
        const href = link.getAttribute('href');
        if (!href || !href.startsWith('#')) return;

        const target = document.getElementById(href.slice(1));
        if (!target) return;

        event.preventDefault();
        scrollToHeading(target);
        setActiveLink(target.id);
    }

    // Set up IntersectionObserver for scroll tracking
    const observerOptions = {
        rootMargin: OBSERVER_ROOT_MARGIN,
        threshold: 0
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                setActiveLink(entry.target.id);
            }
        });
    }, observerOptions);

    // Observe all headings
    headings.forEach(function (heading) {
        observer.observe(heading);
    });

    // Set up click handlers for smooth scrolling
    tocLinks.forEach(function (link) {
        link.addEventListener('click', function (event) {
            handleTocClick(event, link);
        });
    });

    // Set initial active state
    setInitialActive();
})();
