const ROWS = 20;
const COLS = 10;
const BLOCK_SIZE = 30;

const gameBoard = document.getElementById('game-board');
const scoreElement = document.getElementById('score');
const startButton = document.getElementById('start-button');

let board = [];
let currentPiece;
let score = 0;
let gameInterval;
let gameSpeed = 1000; // 初始速度为1秒
let nextPiece;

function createBoard() {
    gameBoard.innerHTML = ''; // 清空游戏板
    for (let row = 0; row < ROWS; row++) {
        board[row] = [];
        for (let col = 0; col < COLS; col++) {
            const cell = document.createElement('div');
            cell.style.width = `${BLOCK_SIZE}px`;
            cell.style.height = `${BLOCK_SIZE}px`;
            cell.style.border = '1px solid #ddd';
            cell.style.boxSizing = 'border-box';
            gameBoard.appendChild(cell);
            board[row][col] = { cell, filled: false };
        }
    }
    gameBoard.style.width = `${COLS * BLOCK_SIZE}px`;
    gameBoard.style.height = `${ROWS * BLOCK_SIZE}px`;
}

function startGame() {
    resetGame();
    createBoard();
    createNewPiece();
    gameInterval = setInterval(gameLoop, gameSpeed);
    startButton.disabled = true;
}

function resetGame() {
    clearInterval(gameInterval);
    board.forEach(row => row.forEach(cell => {
        cell.filled = false;
        cell.cell.style.backgroundColor = '';
    }));
    score = 0;
    scoreElement.textContent = score;
}

function createNewPiece() {
    if (nextPiece) {
        currentPiece = nextPiece;
    } else {
        currentPiece = generateRandomPiece();
    }
    nextPiece = generateRandomPiece();
    updateNextPiecePreview();
    
    currentPiece.row = 0;
    currentPiece.col = Math.floor(COLS / 2) - 1;
    
    if (!canMovePiece(0, 0)) {
        return false;
    }
    return true;
}

function generateRandomPiece() {
    const pieces = [
        [[1, 1, 1, 1]],
        [[1, 1], [1, 1]],
        [[1, 1, 1], [0, 1, 0]],
        [[1, 1, 1], [1, 0, 0]],
        [[1, 1, 1], [0, 0, 1]],
        [[1, 1, 0], [0, 1, 1]],
        [[0, 1, 1], [1, 1, 0]]
    ];
    return {
        shape: pieces[Math.floor(Math.random() * pieces.length)],
        color: getRandomColor()
    };
}

function updateNextPiecePreview() {
    const previewElement = document.getElementById('next-piece-preview');
    previewElement.innerHTML = '';
    previewElement.style.display = 'grid';
    previewElement.style.gridTemplateColumns = `repeat(${nextPiece.shape[0].length}, ${BLOCK_SIZE}px)`;
    
    for (let row = 0; row < nextPiece.shape.length; row++) {
        for (let col = 0; col < nextPiece.shape[row].length; col++) {
            const cell = document.createElement('div');
            cell.style.width = `${BLOCK_SIZE}px`;
            cell.style.height = `${BLOCK_SIZE}px`;
            cell.style.border = '1px solid #ddd';
            cell.style.backgroundColor = nextPiece.shape[row][col] ? nextPiece.color : '';
            previewElement.appendChild(cell);
        }
    }
}

function getRandomColor() {
    const colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF'];
    return colors[Math.floor(Math.random() * colors.length)];
}

function gameLoop() {
    if (canMovePiece(1, 0)) {
        movePiece(1, 0);
    } else {
        placePiece();
        clearLines();
        if (!createNewPiece()) {
            gameOver();
            return;
        }
    }
    drawBoard();
}

function canMovePiece(rowOffset, colOffset) {
    for (let row = 0; row < currentPiece.shape.length; row++) {
        for (let col = 0; col < currentPiece.shape[row].length; col++) {
            if (currentPiece.shape[row][col]) {
                const newRow = currentPiece.row + row + rowOffset;
                const newCol = currentPiece.col + col + colOffset;
                if (newRow >= ROWS || newCol < 0 || newCol >= COLS || 
                    (newRow >= 0 && board[newRow][newCol].filled)) {
                    return false;
                }
            }
        }
    }
    return true;
}

function movePiece(rowOffset, colOffset) {
    currentPiece.row += rowOffset;
    currentPiece.col += colOffset;
}

function placePiece() {
    for (let row = 0; row < currentPiece.shape.length; row++) {
        for (let col = 0; col < currentPiece.shape[row].length; col++) {
            if (currentPiece.shape[row][col]) {
                const boardRow = currentPiece.row + row;
                const boardCol = currentPiece.col + col;
                board[boardRow][boardCol].filled = true;
                board[boardRow][boardCol].cell.style.backgroundColor = currentPiece.color;
            }
        }
    }
}

function clearLines() {
    for (let row = ROWS - 1; row >= 0; row--) {
        if (board[row].every(cell => cell.filled)) {
            for (let r = row; r > 0; r--) {
                for (let col = 0; col < COLS; col++) {
                    board[r][col].filled = board[r-1][col].filled;
                    board[r][col].cell.style.backgroundColor = board[r-1][col].cell.style.backgroundColor;
                }
            }
            score += 100;
            scoreElement.textContent = score;
            updateGameSpeed();
            row++;
        }
    }
}

function drawBoard() {
    board.forEach(row => row.forEach(cell => {
        cell.cell.style.backgroundColor = cell.filled ? cell.cell.style.backgroundColor : '';
    }));

    for (let row = 0; row < currentPiece.shape.length; row++) {
        for (let col = 0; col < currentPiece.shape[row].length; col++) {
            if (currentPiece.shape[row][col]) {
                const boardRow = currentPiece.row + row;
                const boardCol = currentPiece.col + col;
                board[boardRow][boardCol].cell.style.backgroundColor = currentPiece.color;
            }
        }
    }
}

function gameOver() {
    clearInterval(gameInterval);
    alert('游戏结束!');
    startButton.disabled = false;
}

document.addEventListener('keydown', (e) => {
    switch (e.key) {
        case 'ArrowLeft':
            if (canMovePiece(0, -1)) movePiece(0, -1);
            break;
        case 'ArrowRight':
            if (canMovePiece(0, 1)) movePiece(0, 1);
            break;
        case 'ArrowDown':
            if (canMovePiece(1, 0)) movePiece(1, 0);
            break;
        case 'ArrowUp':
            rotatePiece();
            break;
    }
    drawBoard();
});

function rotatePiece() {
    const rotated = currentPiece.shape[0].map((_, i) =>
        currentPiece.shape.map(row => row[i]).reverse()
    );
    const originalShape = currentPiece.shape;
    currentPiece.shape = rotated;
    
    // 尝试基本旋转
    if (canMovePiece(0, 0)) return;
    
    // 尝试向左移动
    if (canMovePiece(0, -1)) {
        currentPiece.col -= 1;
        return;
    }
    
    // 尝试向右移动
    if (canMovePiece(0, 1)) {
        currentPiece.col += 1;
        return;
    }
    
    // 如果都不行，恢复原始形状
    currentPiece.shape = originalShape;
}

function updateGameSpeed() {
    gameSpeed = Math.max(100, 1000 - Math.floor(score / 500) * 100);
    clearInterval(gameInterval);
    gameInterval = setInterval(gameLoop, gameSpeed);
}

createBoard();
startButton.addEventListener('click', startGame);

// 在文件末尾添加以下代码
document.getElementById('to-2048').addEventListener('click', () => {
    window.location.href = '2048.html';
});