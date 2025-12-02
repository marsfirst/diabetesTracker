/**
 * SCHEDULER.JS - Priority Scheduler Demo
 * Demonstrates scheduling concepts from Computer Organization & Architecture
 */

const API_BASE = 'http://127.0.0.1:5000';

/**
 * Helper function to make API calls
 */
async function schedulerApiFetch(path, options = {}) {
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
 * Refresh scheduler queue and history
 */
async function refreshScheduler() {
    try {
        const data = await schedulerApiFetch('/api/scheduler', { method: 'GET' });

        if (data.ok) {
            // Update queue
            const queueList = document.getElementById('queueList');
            if (data.queue.length > 0) {
                let html = '<ol style="font-size: 18px; line-height: 1.8;">';
                data.queue.forEach(task => {
                    const priority = task.priority <= 3 ? '🔴 HIGH' : 
                                   task.priority <= 7 ? '🟡 MEDIUM' : '🟢 LOW';
                    html += `
                        <li style="margin-bottom: 15px; padding: 15px; background: white; border-radius: 6px;">
                            <strong>${task.name}</strong> | 
                            Priority: ${task.priority} ${priority} | 
                            Ticks: ${task.ticks}
                        </li>
                    `;
                });
                html += '</ol>';
                queueList.innerHTML = html;
            } else {
                queueList.innerHTML = '<p>Queue is empty</p>';
            }

            // Update history
            const historyList = document.getElementById('historyList');
            if (data.history.length > 0) {
                let html = '<ol style="font-size: 18px; line-height: 1.8;" start="' + (data.history.length) + '" reversed>';
                data.history.reverse().forEach(task => {
                    html += `
                        <li style="margin-bottom: 15px; padding: 15px; background: #f8f9fa; border-radius: 6px;">
                            <strong>${task.name}</strong> | 
                            Priority: ${task.priority} | 
                            Executed at: ${new Date(task.executed_at).toLocaleTimeString()}
                        </li>
                    `;
                });
                html += '</ol>';
                historyList.innerHTML = html;
            } else {
                historyList.innerHTML = '<p>No tasks executed yet</p>';
            }

            printDebug(`Queue size: ${data.queue.length}, History size: ${data.history.length}`);
        }
    } catch (error) {
        printDebug(`Error: ${error.message}`);
    }
}

/**
 * Submit a new task to the scheduler
 */
async function submitTask() {
    try {
        const name = document.getElementById('taskName').value.trim();
        const priority = parseInt(document.getElementById('priority').value);
        const ticks = parseInt(document.getElementById('ticks').value);

        if (!name) {
            alert('Please enter a task name');
            return;
        }

        if (isNaN(priority) || priority < 1 || priority > 10) {
            alert('Priority must be between 1 and 10');
            return;
        }

        if (isNaN(ticks) || ticks < 1) {
            alert('Ticks must be at least 1');
            return;
        }

        printDebug(`Submitting task: "${name}" | Priority: ${priority} | Ticks: ${ticks}`);

        const data = await schedulerApiFetch('/api/scheduler', {
            method: 'POST',
            body: JSON.stringify({ name, priority, ticks })
        });

        if (data.ok) {
            printDebug(`✓ Task "${name}" added to queue`);
            document.getElementById('taskName').value = '';
            document.getElementById('priority').value = 5;
            document.getElementById('ticks').value = 1;
            await refreshScheduler();
        } else {
            printDebug(`Error: ${data.error}`);
        }
    } catch (error) {
        printDebug(`Error: ${error.message}`);
    }
}

/**
 * Run the scheduler for n ticks
 */
async function runScheduler() {
    try {
        const ticks = parseInt(document.getElementById('runTicks').value);

        if (isNaN(ticks) || ticks < 1) {
            alert('Ticks must be at least 1');
            return;
        }

        printDebug(`\n🏃 Running scheduler for ${ticks} tick(s)...`);

        const data = await schedulerApiFetch(`/api/scheduler/run?ticks=${ticks}`, {
            method: 'POST'
        });

        if (data.ok) {
            data.executed.forEach(task => {
                printDebug(`  → Executed: "${task.name}" (Priority: ${task.priority}, Ticks remaining: ${task.ticks})`);
            });
            printDebug(`✓ Completed ${data.executed.length} task execution(s)`);
            printDebug(`Queue size after run: ${data.queue.length}`);
            await refreshScheduler();
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
 * Initialize scheduler demo on page load
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('⏱️ Scheduler Demo loaded');
    refreshScheduler();
    
    // Add example messages
    printDebug('Welcome to the Priority Scheduler Demo!');
    printDebug('1. Submit a new task with a priority (1=high, 10=low)');
    printDebug('2. Click "Run Ticks" to execute tasks in priority order');
    printDebug('3. Lower priority numbers execute first (min-heap)');
    printDebug('4. Watch the queue and history update in real-time');
});
