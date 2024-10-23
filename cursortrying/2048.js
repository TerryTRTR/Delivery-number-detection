const GRID_SIZE = 4;
const CELL_SIZE = 100;
const CELL_GAP = 15;

const gameBoard = document.getElementById('game-board');
const scoreElement = document.getElementById('score');

let board;
let score;
let isMoving = false;

function initGame() {
    board = Array(GRID_SIZE).fill().map(() => Array(GRID_SIZE).fill(0));
    score = 0;
    addNewTile();
    addNewTile();
    updateBoard();
}

function addNewTile() {
    const emptyTiles = [];
    for (let i = 0; i < GRID_SIZE; i++) {
        for (let j = 0; j < GRID_SIZE; j++) {
            if (board[i][j] === 0) {
                emptyTiles.push({row: i, col: j});
            }
        }
    }
    if (emptyTiles.length > 0) {
        const {row, col} = emptyTiles[Math.floor(Math.random() * emptyTiles.length)];
        board[row][col] = Math.random() < 0.9 ? 2 : 4;
    }
}

function updateBoard() {
    gameBoard.innerHTML = '';
    for (let i = 0; i < GRID_SIZE; i++) {
        for (let j = 0; j < GRID_SIZE; j++) {
            if (board[i][j] !== 0) {
                const tile = document.createElement('div');
                tile.className = `tile tile-${board[i][j]}`;
                tile.textContent = board[i][j];
                tile.style.left = `${j * (CELL_SIZE + CELL_GAP) + CELL_GAP}px`;
                tile.style.top = `${i * (CELL_SIZE + CELL_GAP) + CELL_GAP}px`;
                gameBoard.appendChild(tile);
            }
        }
    }
    scoreElement.textContent = score;
}

function getTileColor(value) {
    const colors = {
        2: '#eee4da',
        4: '#ede0c8',
        8: '#f2b179',
        16: '#f59563',
        32: '#f67c5f',
        64: '#f65e3b',
        128: '#edcf72',
        256: '#edcc61',
        512: '#edc850',
        1024: '#edc53f',
        2048: '#edc22e'
    };
    return colors[value] || '#3c3a32';
}

function checkWin() {
    for (let i = 0; i < GRID_SIZE; i++) {
        for (let j = 0; j < GRID_SIZE; j++) {
            if (board[i][j] === 2048) {
                alert('恭喜你赢了！');
                return true;
            }
        }
    }
    return false;
}

function moveTiles(newBoard) {
    const tiles = document.querySelectorAll('.tile');
    const tileMap = new Map();

    // 创建一个映射，用于跟踪每个值的所有方块
    tiles.forEach(tile => {
        const value = parseInt(tile.textContent);
        if (!tileMap.has(value)) {
            tileMap.set(value, []);
        }
        tileMap.get(value).push(tile);
    });

    for (let i = 0; i < GRID_SIZE; i++) {
        for (let j = 0; j < GRID_SIZE; j++) {
            const newValue = newBoard[i][j];
            if (newValue !== 0) {
                const tilesWithValue = tileMap.get(newValue) || [];
                if (tilesWithValue.length > 0) {
                    const tile = tilesWithValue.pop();
                    tile.style.zIndex = 1;
                    tile.style.left = `${j * (CELL_SIZE + CELL_GAP) + CELL_GAP}px`;
                    tile.style.top = `${i * (CELL_SIZE + CELL_GAP) + CELL_GAP}px`;
                    tile.textContent = newValue;
                    tile.className = `tile tile-${newValue}`;
                } else {
                    // 如果没有现有的方块，创建一个新的
                    const tile = document.createElement('div');
                    tile.className = `tile tile-${newValue} tile-new`;
                    tile.textContent = newValue;
                    tile.style.left = `${j * (CELL_SIZE + CELL_GAP) + CELL_GAP}px`;
                    tile.style.top = `${i * (CELL_SIZE + CELL_GAP) + CELL_GAP}px`;
                    gameBoard.appendChild(tile);
                }
            }
        }
    }

    // 移除所有未使用的方块
    tiles.forEach(tile => {
        if (tile.style.zIndex !== '1') {
            tile.remove();
        } else {
            tile.style.zIndex = '';
        }
    });
}

function move(direction) {
    if (isMoving) return;
    isMoving = true;

    let hasChanged = false;
    const newBoard = JSON.parse(JSON.stringify(board));

    for (let i = 0; i < GRID_SIZE; i++) {
        let row = newBoard[i];
        if (direction === 'ArrowLeft' || direction === 'ArrowRight') {
            row = direction === 'ArrowLeft' ? row : row.reverse();
            const newRow = slide(row);
            newBoard[i] = direction === 'ArrowLeft' ? newRow : newRow.reverse();
        } else {
            let col = newBoard.map(r => r[i]);
            col = direction === 'ArrowUp' ? col : col.reverse();
            const newCol = slide(col);
            for (let j = 0; j < GRID_SIZE; j++) {
                newBoard[j][i] = direction === 'ArrowUp' ? newCol[j] : newCol[GRID_SIZE - 1 - j];
            }
        }
    }

    hasChanged = JSON.stringify(board) !== JSON.stringify(newBoard);
    if (hasChanged) {
        moveTiles(newBoard);
        setTimeout(() => {
            board = newBoard;
            addNewTile();
            updateBoard();
            if (checkWin()) {
                if (confirm('你已经达到2048！要继续游戏吗？')) {
                    isMoving = false;
                } else {
                    initGame();
                }
            } else if (!canMove()) {
                alert('游戏结束！');
                isMoving = false;
            } else {
                isMoving = false;
            }
        }, 150); // 等待动画完成
    } else {
        isMoving = false;
    }
}

function slide(row) {
    let newRow = row.filter(tile => tile !== 0);
    for (let i = 0; i < newRow.length - 1; i++) {
        if (newRow[i] === newRow[i + 1]) {
            newRow[i] *= 2;
            score += newRow[i];
            newRow[i + 1] = 0;
        }
    }
    newRow = newRow.filter(tile => tile !== 0);
    while (newRow.length < GRID_SIZE) {
        newRow.push(0);
    }
    return newRow;
}

function canMove() {
    for (let i = 0; i < GRID_SIZE; i++) {
        for (let j = 0; j < GRID_SIZE; j++) {
            if (board[i][j] === 0) return true;
            if (i < GRID_SIZE - 1 && board[i][j] === board[i + 1][j]) return true;
            if (j < GRID_SIZE - 1 && board[i][j] === board[i][j + 1]) return true;
        }
    }
    return false;
}

document.addEventListener('keydown', event => {
    if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(event.key) && !isMoving) {
        event.preventDefault();
        isMoving = true;
        move(event.key);
        setTimeout(() => {
            isMoving = false;
        }, 100);
    }
});

document.getElementById('new-game').addEventListener('click', initGame);
document.getElementById('to-tetris').addEventListener('click', () => {
    window.location.href = 'index.html';
});

initGame();
