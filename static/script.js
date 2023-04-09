class Game {
  constructor(boardID, timeLimit = 60) {
    this.boardID = boardID;
    this.timeLimit = timeLimit;
    this.words = new Set();
    this.$game = $("#game");
    this.$board = $("#board");
    this.$wordSubmit = $("#submit-word");
    this.$inputWord = $("#word");
    this.$msgs = $("#msgs-box");
    this.$scoreBoard = $("#score");
    this.$words = $("#submitted-words");

    this.$wordSubmit.on("submit", this.handleSubmit.bind(this));
  }
  async handleSubmit(evt) {
    evt.preventDefault();
    const word = this.$inputWord.val();
    const response = await axios.get("/check-word", {
      params: { word: word },
    });
    const result = response.data;
    this.handleResult(result, word);
    this.updateWords();
    console.log(result);
  }
  handleResult(result, word) {
    if (result === "not-word") {
    } else if (result === "not-on-board") {
    } else if (result === "already-used") {
    } else {
    }
  }
  async updateWords() {
    const res = await axios.get("/get-words");
    const words = res.data;
    this.$words.empty();
    for (let word of words) {
      const $listWord = $("<li>").text(word);
      this.$words.append($listWord);
    }
  }
}
const game = new Game("board", 60);
