"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Greeter = void 0;
// src/greeter.ts
class Greeter {
    constructor(name) {
        this.name = name;
    }
    greet() {
        return `Hello, ${this.name}!`;
    }
}
exports.Greeter = Greeter;
