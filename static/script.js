class Game {
  constructor() {
    this.timeLimit = 60;
    this.compliments = [
      "Nice!",
      "Great job!",
      "That's a word!",
      "You found a word!",
      "Perfect!",
    ];

    this.$timer = $("#timer");
    this.$wordSubmit = $("#submit-word");
    this.$inputWord = $("#word");
    this.$msgs = $("#msgs-box");
    this.$scoreBoard = $("#score");
    this.$words = $("#submitted-words");

    this.timer = setInterval(this.handleTimer.bind(this), 1000);

    this.$wordSubmit.on("submit", this.handleSubmit.bind(this));
  }

  async handleTimer() {
    this.timeLimit -= 1;
    this.updateTimer();

    if (this.timeLimit === 0) {
      clearInterval(this.timer);
      await this.endGame();
    }
  }

  async handleSubmit(evt) {
    evt.preventDefault();

    const word = this.$inputWord.val();
    const response = await axios.get("/check-word", {
      params: { word: word },
    });
    const result = response.data;

    this.handleResult(result.result, word);
    this.$inputWord.val("");
  }

  handleResult(result, word) {
    if (result === "not-word") {
      this.showMsg("Sorry! That's not a word!");
    } else if (result === "not-on-board") {
      this.showMsg("Sorry! That word is not on the board!");
    } else if (result === "already-used") {
      this.showMsg("Sorry! You've already used that word!");
    } else {
      const compliment = this.getCompliment();
      this.showMsg(compliment);
      this.updateWords();
      this.updateScore(word.length);
    }
  }
  getCompliment() {
    const rndmCompliment =
      this.compliments[Math.floor(Math.random() * this.compliments.length)];
    return rndmCompliment;
  }
  showMsg(msg) {
    this.$msgs.text(msg);
  }
  updateTimer() {
    this.$timer.text(this.timeLimit);
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
  async updateScore(wordScore) {
    const getScore = await axios.get("/get-score");
    const score = getScore.data + wordScore;
    const postScore = await axios.post("/post-score", { score: score });
    this.$scoreBoard.text(score);
  }
  async endGame() {
    document.location.href = "/end-game?endgame=endgame";
  }
}

const game = new Game();
