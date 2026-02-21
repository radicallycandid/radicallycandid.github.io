/**
 * Theme toggle functionality for light/dark mode support.
 *
 * Features:
 * - Respects system preference (prefers-color-scheme)
 * - Persists user preference in localStorage
 * - Creates a toggle button in the top-right corner
 * - Applies theme immediately to prevent flash of wrong theme
 *
 * @module theme
 */
(function () {
    'use strict';

    /** @const {string} Key used to store theme preference in localStorage */
    const STORAGE_KEY = 'theme-preference';

    /**
     * Get the user's color preference.
     * Checks localStorage first, then falls back to system preference.
     *
     * @returns {'light' | 'dark'} The preferred color theme.
     */
    function getColorPreference() {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) {
            return stored;
        }
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    /**
     * Save and apply a theme preference.
     *
     * @param {'light' | 'dark'} theme - The theme to set.
     */
    function setPreference(theme) {
        localStorage.setItem(STORAGE_KEY, theme);
        reflectPreference(theme);
    }

    /**
     * Apply a theme to the document.
     * Sets the data-theme attribute on the root element.
     *
     * @param {'light' | 'dark'} theme - The theme to apply.
     */
    function reflectPreference(theme) {
        document.documentElement.setAttribute('data-theme', theme);
    }

    /**
     * Create and insert the theme toggle button.
     * Button displays sun/moon icons and toggles between themes on click.
     */
    function createToggleButton() {
        const toggle = document.createElement('button');
        toggle.className = 'theme-toggle';
        toggle.setAttribute('aria-label', 'Toggle theme');
        toggle.innerHTML = '<span class="sun">&#9788;</span><span class="moon">&#9789;</span>';
        document.body.appendChild(toggle);

        toggle.addEventListener('click', function () {
            const current = document.documentElement.getAttribute('data-theme') || getColorPreference();
            const next = current === 'dark' ? 'light' : 'dark';
            setPreference(next);
        });
    }

    // Set theme immediately to prevent flash of unstyled content
    reflectPreference(getColorPreference());

    // Create toggle button once DOM is ready
    window.addEventListener('DOMContentLoaded', createToggleButton);

    // Sync with system preference changes (only if user hasn't set a preference)
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (event) {
        if (!localStorage.getItem(STORAGE_KEY)) {
            reflectPreference(event.matches ? 'dark' : 'light');
        }
    });
})();
