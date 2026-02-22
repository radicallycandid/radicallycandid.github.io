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
        toggle.innerHTML =
            '<span class="sun"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg></span>' +
            '<span class="moon"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg></span>';
        var nav = document.querySelector('.site-nav');
        if (nav) {
            nav.appendChild(toggle);
        } else {
            document.body.appendChild(toggle);
        }

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
