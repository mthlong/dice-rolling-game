// Global variables
let currentUsername = '';
let hasRolled = false;
const API_BASE_URL = '/api';

// Dice face icons mapping
const diceIcons = {
    1: 'fas fa-dice-one',
    2: 'fas fa-dice-two',
    3: 'fas fa-dice-three',
    4: 'fas fa-dice-four',
    5: 'fas fa-dice-five',
    6: 'fas fa-dice-six'
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Focus on username input
    document.getElementById('usernameInput').focus();
    
    // Add enter key listener for username input
    document.getElementById('usernameInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            startGame();
        }
    });
    
    // Load initial data
    loadRankings();
    loadHistory();
});

// Start the game with username
function startGame() {
    const usernameInput = document.getElementById('usernameInput');
    const username = usernameInput.value.trim();
    const errorDiv = document.getElementById('usernameError');
    
    // Validate username
    if (!username) {
        showError(errorDiv, 'Please enter a username');
        return;
    }
    
    if (username.length < 2) {
        showError(errorDiv, 'Username must be at least 2 characters long');
        return;
    }
    
    if (!/^[a-zA-Z0-9_]+$/.test(username)) {
        showError(errorDiv, 'Username can only contain letters, numbers, and underscores');
        return;
    }
    
    currentUsername = username;
    
    // Hide modal and show game interface
    document.getElementById('usernameModal').classList.add('hidden');
    document.getElementById('gameInterface').classList.remove('hidden');
    document.getElementById('currentUsername').textContent = username;
    
    // Check if user has already rolled
    checkUserRollStatus();
}

// Check if user has already rolled dice
async function checkUserRollStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/dice/check/${currentUsername}`);
        const data = await response.json();
        
        if (data.has_rolled) {
            hasRolled = true;
            const rollButton = document.getElementById('rollDiceBtn');
            rollButton.disabled = true;
            rollButton.innerHTML = '<i class="fas fa-check"></i> Already Rolled!';
            
            // Display the existing roll
            if (data.roll) {
                displayDiceResult(data.roll.dice1, data.roll.dice2, data.roll.dice3, data.roll.total_score);
                showRollResult(`You already rolled: ${data.roll.dice1}, ${data.roll.dice2}, ${data.roll.dice3} = ${data.roll.total_score}`, 'success');
            }
        }
    } catch (error) {
        console.error('Error checking roll status:', error);
    }
}

// Roll the dice
async function rollDice() {
    if (hasRolled) {
        showRollResult('You have already rolled the dice!', 'error');
        return;
    }
    
    const rollButton = document.getElementById('rollDiceBtn');
    const loadingOverlay = document.getElementById('loadingOverlay');
    
    // Show loading
    loadingOverlay.classList.remove('hidden');
    rollButton.disabled = true;
    
    // Animate dice rolling
    animateDiceRoll();
    
    try {
        const response = await fetch(`${API_BASE_URL}/dice/roll`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username: currentUsername })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Success
            const roll = data.roll;
            hasRolled = true;
            
            // Wait for animation to complete
            setTimeout(() => {
                displayDiceResult(roll.dice1, roll.dice2, roll.dice3, roll.total_score);
                showRollResult(`Great roll! You got: ${roll.dice1}, ${roll.dice2}, ${roll.dice3} = ${roll.total_score}`, 'success');
                
                rollButton.innerHTML = '<i class="fas fa-check"></i> Already Rolled!';
                loadingOverlay.classList.add('hidden');
                
                // Refresh rankings and history
                loadRankings();
                loadHistory();
            }, 1000);
        } else {
            // Error
            loadingOverlay.classList.add('hidden');
            rollButton.disabled = false;
            showRollResult(data.error || 'Failed to roll dice', 'error');
        }
    } catch (error) {
        console.error('Error rolling dice:', error);
        loadingOverlay.classList.add('hidden');
        rollButton.disabled = false;
        showRollResult('Network error. Please try again.', 'error');
    }
}

// Animate dice rolling
function animateDiceRoll() {
    const dice = document.querySelectorAll('.dice');
    
    dice.forEach(die => {
        die.classList.add('rolling');
        
        // Change dice faces randomly during animation
        const interval = setInterval(() => {
            const randomFace = Math.floor(Math.random() * 6) + 1;
            die.querySelector('i').className = diceIcons[randomFace];
        }, 100);
        
        // Stop animation after 1 second
        setTimeout(() => {
            die.classList.remove('rolling');
            clearInterval(interval);
        }, 1000);
    });
}

// Display dice result
function displayDiceResult(dice1, dice2, dice3, totalScore) {
    // Update dice faces
    document.querySelector('#dice1 i').className = diceIcons[dice1];
    document.querySelector('#dice2 i').className = diceIcons[dice2];
    document.querySelector('#dice3 i').className = diceIcons[dice3];
    
    // Update total score
    document.getElementById('totalScore').textContent = totalScore;
}

// Show roll result message
function showRollResult(message, type) {
    const resultDiv = document.getElementById('rollResult');
    resultDiv.textContent = message;
    resultDiv.className = `roll-result ${type}`;
    resultDiv.classList.remove('hidden');
}

// Load rankings from API
async function loadRankings() {
    try {
        const response = await fetch(`${API_BASE_URL}/rankings`);
        const rankings = await response.json();
        
        const rankingsList = document.getElementById('rankingsList');
        
        if (rankings.length === 0) {
            rankingsList.innerHTML = '<div class="loading">No rankings yet. Be the first to roll!</div>';
            return;
        }
        
        rankingsList.innerHTML = rankings.map(ranking => `
            <div class="ranking-item ${ranking.is_highlighted ? 'highlighted' : ''}">
                <div class="rank-number">${ranking.rank}</div>
                <div class="player-name">${ranking.username}</div>
                <div class="player-score">${ranking.highest_score}</div>
            </div>
        `).join('');
        
    } catch (error) {
        console.error('Error loading rankings:', error);
        document.getElementById('rankingsList').innerHTML = '<div class="loading">Error loading rankings</div>';
    }
}

// Load history from API
async function loadHistory() {
    try {
        const response = await fetch(`${API_BASE_URL}/sheets/history`);
        const history = await response.json();
        
        const historyList = document.getElementById('historyList');
        
        if (history.length === 0) {
            historyList.innerHTML = '<div class="loading">No rolls yet. Start playing!</div>';
            return;
        }
        
        // Sort by timestamp (newest first) and take last 10
        const sortedHistory = history.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)).slice(0, 10);
        
        historyList.innerHTML = sortedHistory.map(roll => `
            <div class="history-item">
                <div class="history-player">
                    <i class="fas fa-user"></i> ${roll.username}
                </div>
                <div class="history-dice">
                    <div class="history-dice-value">${roll.dice1}</div>
                    <div class="history-dice-value">${roll.dice2}</div>
                    <div class="history-dice-value">${roll.dice3}</div>
                </div>
                <div class="history-score">
                    Total: ${roll.total_score}
                </div>
                <div class="history-time">
                    ${formatDateTime(roll.timestamp)}
                </div>
            </div>
        `).join('');
        
    } catch (error) {
        console.error('Error loading history:', error);
        document.getElementById('historyList').innerHTML = '<div class="loading">Error loading history</div>';
    }
}

// Format date and time
function formatDateTime(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Show error message
function showError(element, message) {
    element.textContent = message;
    element.style.display = 'block';
    setTimeout(() => {
        element.style.display = 'none';
    }, 3000);
}

// Refresh data periodically
setInterval(() => {
    if (!document.getElementById('gameInterface').classList.contains('hidden')) {
        loadRankings();
        loadHistory();
    }
}, 30000); // Refresh every 30 seconds

