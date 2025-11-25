// Crossword puzzle interactivity
document.addEventListener('DOMContentLoaded', function() {
  const grid = document.querySelector('.puzzle-grid');
  if (!grid) return;
  
  const inputs = grid.querySelectorAll('input');
  
  // Keyboard navigation
  inputs.forEach((input, index) => {
    input.addEventListener('keydown', function(e) {
      const row = parseInt(input.dataset.r);
      const col = parseInt(input.dataset.c);
      let nextInput = null;
      
      switch(e.key) {
        case 'ArrowRight':
          nextInput = grid.querySelector(`input[data-r="${row}"][data-c="${col + 1}"]`);
          break;
        case 'ArrowLeft':
          nextInput = grid.querySelector(`input[data-r="${row}"][data-c="${col - 1}"]`);
          break;
        case 'ArrowDown':
          nextInput = grid.querySelector(`input[data-r="${row + 1}"][data-c="${col}"]`);
          break;
        case 'ArrowUp':
          nextInput = grid.querySelector(`input[data-r="${row - 1}"][data-c="${col}"]`);
          break;
        case 'Backspace':
          if (input.value === '') {
            nextInput = grid.querySelector(`input[data-r="${row}"][data-c="${col - 1}"]`);
          }
          break;
      }
      
      if (nextInput) {
        e.preventDefault();
        nextInput.focus();
      }
    });
    
    input.addEventListener('input', function(e) {
      const val = input.value.toUpperCase();
      input.value = val;
      
      if (val.length === 1) {
        const row = parseInt(input.dataset.r);
        const col = parseInt(input.dataset.c);
        const nextInput = grid.querySelector(`input[data-r="${row}"][data-c="${col + 1}"]`);
        if (nextInput) {
          nextInput.focus();
        }
      }
    });
  });
  
  // Check puzzle button
  const checkBtn = document.getElementById('checkPuzzle');
  if (checkBtn) {
    checkBtn.addEventListener('click', function() {
      let correct = 0;
      let total = 0;
      
      inputs.forEach(input => {
        const answer = input.dataset.answer;
        const value = input.value.toUpperCase();
        
        if (value) {
          total++;
          if (value === answer) {
            input.classList.add('correct');
            input.classList.remove('incorrect');
            correct++;
          } else {
            input.classList.add('incorrect');
            input.classList.remove('correct');
          }
        }
      });
      
      if (total === 0) {
        alert('Please fill in some answers first!');
      } else if (correct === inputs.length) {
        alert('🎉 Congratulations! You solved the puzzle correctly!');
      } else {
        alert(`You have ${correct} out of ${total} filled cells correct. Keep going!`);
      }
    });
  }
  
  // Show solution button
  const showBtn = document.getElementById('showSolution');
  if (showBtn) {
    showBtn.addEventListener('click', function() {
      const solution = document.getElementById('solution');
      if (solution) {
        if (solution.style.display === 'none') {
          solution.style.display = 'block';
          showBtn.textContent = 'Hide Solution';
        } else {
          solution.style.display = 'none';
          showBtn.textContent = 'Show Solution';
        }
      }
    });
  }
});

// Social sharing functions
function shareTwitter() {
  const url = encodeURIComponent(window.location.href);
  const text = encodeURIComponent('Check out this daily crossword puzzle!');
  window.open(`https://twitter.com/intent/tweet?url=${url}&text=${text}`, '_blank', 'width=600,height=400');
}

function shareFacebook() {
  const url = encodeURIComponent(window.location.href);
  window.open(`https://www.facebook.com/sharer/sharer.php?u=${url}`, '_blank', 'width=600,height=400');
}

function shareLinkedIn() {
  const url = encodeURIComponent(window.location.href);
  window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${url}`, '_blank', 'width=600,height=400');
}
