
// class BoggleGame {

//     constructor(id, timer = 60) {
//         this.timer = timer;
//         this.words = [];
//         this.board = $('#'+ id);
//         $('#add_word', this.board).on("submit", this.handle_click.bind(this));
//         console.log(this.board);
//     }

//     // async handleSubmit(evt) {
//     //     evt.preventDefault();
//     //     const $word = $(".word", this.board);
    
//     //     let word = $word.val();
//     //     if (!word) return;
    
//     //     if (this.words.has(word)) {
//     //       this.showMessage(`Already found ${word}`, "err");
//     //       return;
//     //     }
    
//     //     // check server for validity
//     //     const resp = await axios.get("/check-word", { params: { word: word }});
//     //     if (resp.data.result === "not-word") {
//     //       this.showMessage(`${word} is not a valid English word`, "err");
//     //     } else if (resp.data.result === "not-on-board") {
//     //       this.showMessage(`${word} is not a valid word on this board`, "err");
//     //     } else {
//     //       this.showWord(word);
//     //       this.score += word.length;
//     //       this.showScore();
//     //       this.words.add(word);
//     //       this.showMessage(`Added: ${word}`, "ok");
//     //     }
    
//     //     $word.val("").focus();
//     //   }
    
//       /* Update timer in DOM */

//     async send_to_server(word) {
//         const response = await axios.get('/check-word', { params :
//             {word: word}
//         });
//         let status = response.data.result;
//         if (status == 'ok') {
//             console.log("hi");
//             this.show_word(word);
//         } else if (status == 'not-word') {
//             this.show_message(`Word ${word} is not a valid English word`);
//         } else {
//             this.show_message(`Word ${word} is not on this board`);
//         }
//         console.log(response);  
//     }
  
//     async handle_click(evt) {
//         evt.preventDefault();
//         let word = $('input', this.board).val();
//         if(!word) return;

//         if (word in this.words) {
//             this.show_message(`${word} is already in the list`);
//             return;
//         }

//         await this.send_to_server(word);
//         $('input', this.board).val("");
//     }

//     show_word(word) {
//         this.words.push(word);
//         $('#words_list').append($(`<li>${word}</li>`));
//     }

//     show_message(message) {
//         $('.message').text(message);
//     }
// }
const words = [];
let score = 0;
let timer = 60;
let myTimer = setInterval(showTimer , 1000);

//Gets the word from form, sends to server for validation
function handleClick(evt) {
    evt.preventDefault();
    let word = $('input').val();
    if(!word) return;
    
    //Checks if the word already exists
    if (words.indexOf(word.toLowerCase()) != -1) {
        showMessage(`"${word}" is already in the list`);
        $('input').val("");
        return;
    }
    sendToServer(word);
    $('input').val("");
}

//Checks if it's a valid word and on the board
async function sendToServer(word) {
    const response = await axios.get('/check-word', { params :
        {word: word}
    });
    let status = response.data.result;
    if (status == 'ok') {
        addAndShowWord(word);
        updateScore(word);

    } else if (status == 'not-word') {
        showMessage(`Word "${word}" is not a valid English word`);
    } else {
        showMessage(`Word "${word}" is not on this board`);
    }
}

//Adds the word to the list and shows
function addAndShowWord(word) {
    words.push(word);
    $('#words_list').append($(`<li>${word}</li>`));
}
//Shows messages
function showMessage(message) {
    $('.message').text(message);
}
//Updates score and diplays it
function updateScore(word) {
    score += word.length;
    $("#score_field").text(score);
}

//Shows timer
function showTimer() {
    $('#time_field').text(timer);
    timer --;
    if (timer == 0) {
        endGame();
    }
}


function endGame() {
    clearInterval(myTimer);
    $('#form_field').addClass('hidden');
    checkForRecord();
}

//Checks if final score broke the record, diplays final score
async function checkForRecord() {
    const response = await axios.post('/score', {score : score});
    if (response.data.new_record) {
        showMessage(`New highest score is ${score}!`);
    } else {
        showMessage(`Your final score is ${score}!`);
    }
}

$('#add_word').on("submit", handleClick);

