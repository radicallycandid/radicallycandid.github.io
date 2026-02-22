/**
 * Language preference persistence.
 *
 * When the user clicks the language toggle (an <a> tag), we save their
 * explicit choice to localStorage so the root redirect page can use it.
 * The actual navigation happens via the href — this script only persists
 * the preference.
 *
 * @module lang
 */
(function () {
    'use strict';

    /** @const {string} Key used to store language preference in localStorage */
    var STORAGE_KEY = 'lang-preference';

    window.addEventListener('DOMContentLoaded', function () {
        var link = document.querySelector('.lang-toggle');
        if (!link) return;

        link.addEventListener('click', function () {
            // The href points to the OTHER language, so save that as preference
            var currentLang = document.documentElement.lang;
            var newLang = currentLang === 'pt' ? 'en' : 'pt';
            localStorage.setItem(STORAGE_KEY, newLang);
        });
    });
})();
