
// Read all buttons from table
const buttons = document.querySelectorAll('#tic_tac_toe_table button');

//players turn 
let turn = 'X';
// slice the array into a matrix
const board = [
  Array.from(buttons).slice(0, 3),
  Array.from(buttons).slice(3, 6),
  Array.from(buttons).slice(6, 9)
];

//get clean state board
function getBoardState(){
  return board.map(row => row.map(cell => cell.textContent));
}

//check for winner
function checkWinnerState(state){
  for (let i = 0; i < 3; i++){
    //vertical win
    if (state[0][i] === state[1][i] && state [1][i] === state[2][i] && state[0][i] !== ''){
      return state[0][i];
    }
    //horizontal win
    if (state[i][0] === state[i][1] && state [i][1] === state[i][2] && state[i][0] !== ''){
      return state[i][0];
    }
  }
    //diagonals
  if (state[0][0] === state[1][1] && state[1][1] === state[2][2] && state[0][0] !== ''){
    return state[0][0];
  }
  //reverse diagonals
  if (state[2][0] === state[1][1] && state[1][1] === state[0][2] && state[2][0] !== ''){
    return state[2][0];
  }

  //nobody wins yet
  return null;
}

//check for tie
function checkTie(state){
  //check if not empty cells left and nobody is winning
  return (state.every(row => row.every(cell => cell !== '')) && checkWinnerState(state) == null);
}

//minimax for ai logic
function minimax(state,depth,isMaximizing){
  let winner = checkWinnerState(state);
  //base cases

  //player is winning
  if (winner === 'X'){ return 10 - depth};
  //ai is winning
  if (winner === 'O'){ return depth - 10};
  //tie
  if (checkTie(state)){ return 0;}

  //maximizing branch
  if (isMaximizing){
    let best = -Infinity;
    //check all possible permutations
    for (let i = 0; i < 3; i++){
      for (let j = 0; j < 3; j++){
        if (state[i][j] === ''){
          state[i][j] = 'X';
          let score = minimax(state,depth+1,false);
          best = Math.max(best,score);
          //undo
          state[i][j] = '';
        }
      }
    }
    return best;
  }
  //minimizing branch
  else{
    let best = Infinity;
    //check all possible permutations
    for (let i = 0; i < 3; i++){
      for (let j = 0; j < 3; j++){
        if (state[i][j] === ''){
          state[i][j] = 'O';
          let score = minimax(state,depth+1,true);
          best = Math.min(best,score);
          //undo
          state[i][j] = '';
        }
      }
    }

    return best;
  }
}

//implement minimax to ai
function aiCorrectMove(state){

  //ai is minimizing so:
  let bestScore = Infinity;
  let move = {i: -1, j: -1};

  //check all cells and pick the best option
  for (let i = 0; i < 3; i++){
    for (let j = 0; j < 3; j++){
      if (state[i][j] === ''){
        //try the current cell
        state[i][j] = 'O';
        let score = minimax(state, 0, true);
        //undo move
        state[i][j] = '';
        //ai is minimizing 
        if (score < bestScore){
          bestScore = score;
          move = {i, j};
        }
      }
    }
  }
  //apply the move to the board
  if (move.i !== -1 && move.j !== -1) {
    board[move.i][move.j].textContent = 'O';
  }
}

//random move for ai
function aiRandomMove(state){
  // find empty cells
  const emptyCells = [];
  for (let i = 0; i < 3; i++){
    for (let j = 0; j < 3; j++){
      if (state[i][j] === ''){
        emptyCells.push({i,j});
      }
    }
  }
  // no empty cells → do nothing
  if (emptyCells.length === 0) return;
  // pick a random empty cell
  const move = emptyCells[Math.floor(Math.random() * emptyCells.length)];
  // update the board 
  board[move.i][move.j].textContent = 'O';
}


function aiMove(state){
  //make move based on difficulty
  const difficulty = 60;
  if (Math.random() * 100 < difficulty){
    aiCorrectMove(state)
  }
  else{
    aiRandomMove(state)
  }
}


function resetBoard(){
  buttons.forEach(button => button.textContent = '');
  turn = 'X';
}



buttons.forEach(button => {
  button.addEventListener('click', () => {
    if (button.textContent === '' && turn === 'X') {
      button.textContent = 'X';
      turn = 'O'; // now it's AI's turn

      let state = getBoardState();

      //player wins
      if (checkWinnerState(state) === 'X') {
        alert('Player wins!');
        resetBoard();
        window.location.href = '/';
        return;
      }
      if (checkTie(state)) {
        alert('Tie!');
        resetBoard();
        return;
      }

      setTimeout(() => {
        aiMove(state); // AI makes its move

        state = getBoardState(); // update after AI move

        if (checkWinnerState(state) === 'O') {
          alert('AI wins!');
          resetBoard();
        } else if (checkTie(state)) {
          alert('Tie!');
          resetBoard();
          //player wins
        }else {
          turn = 'X'; // back to player
        }
      }, 100);
    }
  });
});



