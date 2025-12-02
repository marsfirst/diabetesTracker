/**
 * MAIN.JS - Core Functions for Diabetes Tracker
 * Handles API calls, login, and main dashboard functions
 */

const API_BASE = 'http://127.0.0.1:5000';

/**
 * Helper function to make API calls
 */
async function apiFetch(path, options = {}) {
    try {
        const response = await fetch(`${API_BASE}${path}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({ error: 'Unknown error' }));
            throw new Error(error.error || `HTTP ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

/**
 * Login function
 */
async function login(email, pin) {
    try {
        const data = await apiFetch('/api/login', {
            method: 'POST',
            body: JSON.stringify({ email, pin })
        });

        if (data.ok) {
            localStorage.setItem('user_id', data.user.id);
            localStorage.setItem('email', data.user.email);
            return data.user;
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        console.error('Login failed:', error);
        throw error;
    }
}

/**
 * Logout function
 */
async function logout() {
    try {
        const userId = localStorage.getItem('user_id') || 1;
        await apiFetch('/api/logout', {
            method: 'POST',
            body: JSON.stringify({ user_id: userId })
        });

        localStorage.removeItem('user_id');
        localStorage.removeItem('email');
        window.location.href = '/static/login.html';
    } catch (error) {
        console.error('Logout failed:', error);
    }
}

/**
 * Load readings from API
 */
async function loadReadings(limit = 50) {
    try {
        const userId = localStorage.getItem('user_id') || 1;
        const data = await apiFetch(`/api/readings?user_id=${userId}&limit=${limit}`, {
            method: 'GET'
        });

        if (data.ok) {
            return data.readings;
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        console.error('Failed to load readings:', error);
        return [];
    }
}

/**
 * Submit a new reading
 */
async function submitReading(glucose, context, meal, note) {
    try {
        const userId = localStorage.getItem('user_id') || 1;
        const data = await apiFetch('/api/readings', {
            method: 'POST',
            body: JSON.stringify({
                user_id: userId,
                glucose: parseFloat(glucose),
                context,
                meal,
                note
            })
        });

        if (data.ok) {
            return data.reading;
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        console.error('Failed to submit reading:', error);
        throw error;
    }
}

/**
 * Get suggestions based on glucose level
 */
async function getSuggestions(glucose, context = 'general') {
    try {
        const userId = localStorage.getItem('user_id') || 1;
        const data = await apiFetch('/api/suggestions', {
            method: 'POST',
            body: JSON.stringify({
                user_id: userId,
                glucose: parseFloat(glucose),
                context
            })
        });

        if (data.ok) {
            return data;
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        console.error('Failed to get suggestions:', error);
        throw error;
    }
}

/**
 * Test API connectivity
 */
async function testAPI() {
    try {
        const data = await apiFetch('/api/ping', { method: 'GET' });
        console.log('✓ API is online:', data);
        return true;
    } catch (error) {
        console.error('✗ API is offline:', error);
        return false;
    }
}

/**
 * Check if user is logged in
 */
function isLoggedIn() {
    return !!localStorage.getItem('user_id');
}

/**
 * Get current user ID
 */
function getCurrentUserId() {
    return localStorage.getItem('user_id') || 1;
}

/**
 * Initialize page on load
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('📱 Diabetes Tracker loaded');
    testAPI();
});
