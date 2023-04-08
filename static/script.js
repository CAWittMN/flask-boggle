class Game {
  constructor(boardID, timeLimit = 60) {
    this.boardID = boardID;
    this.timeLimit = timeLimit;
    this.$board = $("#board");
    this.$wordSubmit = $("#word");
    this.$msgs = $("#msgs-box");
    this.$scoreBoard = $("#score");
    this.$words = $("#submitted-words");
  }
}
