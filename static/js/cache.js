/**
 * CACHE.JS - LRU Cache Demo
 * Demonstrates cache concepts from Computer Organization & Architecture
 */

const API_BASE = 'http://127.0.0.1:5000';

/**
 * Helper function to make API calls
 */
async function cacheApiFetch(path, options = {}) {
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
 * Load cache statistics
 */
async function refreshCache() {
    try {
        const data = await cacheApiFetch('/api/cache', { method: 'GET' });
        
        if (data.ok) {
            // Update stats
            document.getElementById('capacity').textContent = data.capacity;
            document.getElementById('size').textContent = data.size;
            document.getElementById('hits').textContent = data.hits;
            document.getElementById('misses').textContent = data.misses;

            // Update items list
            const itemsList = document.getElementById('itemsList');
            if (data.items.length > 0) {
                let html = '<ul style="font-size: 18px; line-height: 1.8;">';
                data.items.forEach((item, index) => {
                    const [id, reading] = item;
                    html += `
                        <li style="margin-bottom: 15px; padding: 10px; background: white; border-radius: 6px;">
                            <strong>Reading ID ${id}:</strong> ${reading.glucose} mg/dL 
                            (${reading.context} - ${reading.created_at})
                        </li>
                    `;
                });
                html += '</ul>';
                itemsList.innerHTML = html;
            } else {
                itemsList.innerHTML = '<p>No items in cache</p>';
            }

            printDebug(`Cache refreshed: ${data.size}/${data.capacity} slots, ${data.hits} hits, ${data.misses} misses`);
        }
    } catch (error) {
        printDebug(`Error: ${error.message}`);
    }
}

/**
 * Load a reading into the cache
 */
async function loadToCache() {
    try {
        const readingId = parseInt(document.getElementById('readingId').value);
        
        if (isNaN(readingId) || readingId < 1) {
            alert('Please enter a valid reading ID');
            return;
        }

        printDebug(`Loading reading ${readingId} into cache...`);

        const data = await cacheApiFetch(`/api/cache/put`, {
            method: 'POST',
            body: JSON.stringify({ id: readingId })
        });

        if (data.ok) {
            printDebug(`✓ Reading ${readingId} loaded into cache`);
            printDebug(`Stats: ${data.stats.size}/${data.stats.capacity} slots, ${data.stats.hits} hits, ${data.stats.misses} misses`);
            await refreshCache();
        } else {
            printDebug(`Error: ${data.error}`);
        }
    } catch (error) {
        printDebug(`Error: ${error.message}`);
    }
}

/**
 * Get a reading from cache
 */
async function getCacheItem(readingId) {
    try {
        printDebug(`Accessing reading ${readingId} from cache...`);

        const data = await cacheApiFetch(`/api/cache/get/${readingId}`, { method: 'GET' });

        if (data.ok) {
            const wasHit = data.stats.hits > 0 ? '(cache HIT)' : '(cache MISS)';
            printDebug(`✓ Retrieved reading ${readingId} ${wasHit}`);
            printDebug(`Glucose: ${data.item.glucose} mg/dL`);
            printDebug(`Stats: ${data.stats.size}/${data.stats.capacity} slots, ${data.stats.hits} hits, ${data.stats.misses} misses`);
            await refreshCache();
        } else {
            printDebug(`Error: ${data.error}`);
        }
    } catch (error) {
        printDebug(`Error: ${error.message}`);
    }
}

/**
 * Print to debug output
 */
function printDebug(message) {
    const output = document.getElementById('output');
    output.style.display = 'block';
    const timestamp = new Date().toLocaleTimeString();
    output.innerHTML += `[${timestamp}] ${message}\n`;
    output.scrollTop = output.scrollHeight; // Auto-scroll to bottom
}

/**
 * Clear debug output
 */
function clearDebug() {
    document.getElementById('output').innerHTML = '';
    document.getElementById('output').style.display = 'none';
}

/**
 * Initialize cache demo on page load
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('🔄 Cache Demo loaded');
    refreshCache();
    
    // Add example messages
    printDebug('Welcome to the LRU Cache Demo!');
    printDebug('Enter a reading ID (1-6) to load it into the cache.');
    printDebug('The cache can hold 5 items at a time.');
    printDebug('Watch as items get evicted when cache is full (LRU policy).');
});
