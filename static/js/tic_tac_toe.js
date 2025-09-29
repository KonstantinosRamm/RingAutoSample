
// Read all buttons from table
const buttons = document.querySelectorAll('#tic_tac_toe_table button');

// Create 2D board array
const board = [
  Array.from(buttons).slice(0, 3),
  Array.from(buttons).slice(3, 6),
  Array.from(buttons).slice(6, 9)
];

let turn = 'X'; // Player starts

// Check winner: returns 'X', 'O', or null
function checkWinner(board) {
  for (let i = 0; i < 3; i++) {
    // Rows
    if (
      board[i][0].textContent &&
      board[i][0].textContent === board[i][1].textContent &&
      board[i][1].textContent === board[i][2].textContent
    ) return board[i][0].textContent;

    // Columns
    if (
      board[0][i].textContent &&
      board[0][i].textContent === board[1][i].textContent &&
      board[1][i].textContent === board[2][i].textContent
    ) return board[0][i].textContent;
  }

  // Main diagonal
  if (
    board[0][0].textContent &&
    board[0][0].textContent === board[1][1].textContent &&
    board[1][1].textContent === board[2][2].textContent
  ) return board[0][0].textContent;

  // Anti-diagonal
  if (
    board[0][2].textContent &&
    board[0][2].textContent === board[1][1].textContent &&
    board[1][1].textContent === board[2][0].textContent
  ) return board[0][2].textContent;

  return null; // nobody won
}

// Handle winner or tie
function handleWinnerOrTie() {
  const winner = checkWinner(board);

  if (winner === 'X') {
    window.location.href = "/"; // Player wins → redirect
    return true;
  } else if (winner === 'O') {
    console.log("AI wins! Restarting game...");
    setTimeout(resetBoard, 1000); // AI wins → restart
    return true;
  }

  // Check for tie
  const allFilled = Array.from(buttons).every(b => b.textContent !== '');
  if (allFilled) {
    console.log("It's a tie! Restarting game...");
    setTimeout(resetBoard, 1000); // tie → restart
    return true;
  }

  return false; // Game continues
}

// Player move
function playerMove(button) {
  if (button.textContent === '' && turn === 'X') {
    button.textContent = 'X';

    if (handleWinnerOrTie()) return; // Check winner/tie

    turn = 'O';
    setTimeout(aiMove, 500); // AI plays after 0.5s
  }
}

// AI move (random)
function aiMove() {
  const emptyButtons = Array.from(buttons).filter(b => b.textContent === '');
  if (emptyButtons.length === 0) return;

  const move = emptyButtons[Math.floor(Math.random() * emptyButtons.length)];
  move.textContent = 'O';
  console.log('AI plays');

  if (handleWinnerOrTie()) return; // Check winner/tie

  turn = 'X';
}

// Reset board for new game
function resetBoard() {
  buttons.forEach(b => b.textContent = '');
  turn = 'X';
}

// Add click listener to all buttons
buttons.forEach(button => {
  button.addEventListener('click', () => playerMove(button));
});

