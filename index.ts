// src/index.ts
import { Logger } from './logger';
import { Greeter } from './greeter';

// Create an instance of Greeter
const greeter = new Greeter("World");

// Create a greeting message
const message = greeter.greet();

// Log the greeting message
Logger.log(message);
