"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
// You shouldn't have to modify this code since it only contains the communication between the server and your bot.
// Your code logic should be in ./Bot.ts.
const ws_1 = __importDefault(require("ws"));
const Bot_1 = require("./Bot");
const GameInterface_1 = require("./GameInterface");
const webSocket = new ws_1.default("ws://0.0.0.0:8765");
let bot;
webSocket.onopen = (event) => {
    bot = new Bot_1.Bot();
    if (process.env.TOKEN) {
        webSocket.send(JSON.stringify({ type: "REGISTER", token: process.env.TOKEN }));
    }
    else {
        webSocket.send(JSON.stringify({ type: "REGISTER", teamName: "MyBot TypeScript" }));
    }
};
webSocket.onmessage = (message) => {
    const rawGameMessage = JSON.parse(message.data.toString());
    const gameMessage = new GameInterface_1.GameMessage(rawGameMessage);
    console.log(`Playing tick ${gameMessage.currentTickNumber}`);
    let actions = [];
    // Just so your bot doesn't completely crash. ;)
    try {
        actions = bot.getNextMoves(gameMessage);
    }
    catch (exception) {
        console.log(`Exception while getting next moves: ${exception.stack}`);
    }
    webSocket.send(JSON.stringify({
        type: "COMMAND",
        tick: gameMessage.currentTickNumber,
        actions: actions,
    }));
};
//# sourceMappingURL=index.js.map