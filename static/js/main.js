/**
 * ReviewGuard AI — Main Client-Side JavaScript
 * Provides UI interactivity, auto-dismissing notifications, and CSRF fetch helpers.
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Auto-dismiss flash alerts after 6 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s ease';
            setTimeout(() => alert.remove(), 500);
        }, 6000);
    });

    // 2. Global CSRF Token Helper for AJAX
    const csrfMeta = document.querySelector('meta[name="csrf-token"]');
    const csrfToken = csrfMeta ? csrfMeta.getAttribute('content') : '';

    window.reviewGuardFetch = function(url, options = {}) {
        options.headers = options.headers || {};
        if (csrfToken && !options.headers['X-CSRFToken']) {
            options.headers['X-CSRFToken'] = csrfToken;
        }
        return fetch(url, options);
    };

    // 3. Smooth table row interactions
    const dataTableRows = document.querySelectorAll('.data-table tbody tr');
    dataTableRows.forEach(row => {
        row.addEventListener('mouseenter', () => {
            row.style.transition = 'background-color 0.15s ease';
        });
    });

    console.log("ReviewGuard AI Interface Initialized.");
});
