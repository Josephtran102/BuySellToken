import { ethers } from 'ethers';
let playSound;
// Dynamic import of play-sound module
import('play-sound').then(module => {
  playSound = module.default({});
}).catch(error => console.error('Cannot load the play-sound module', error));

const reset = "\x1b[0m";
const green = "\x1b[32m";
const blue = "\x1b[34m";
const red = "\x1b[31m";
const grey = "\x1b[90m";
const yellow = "\x1b[33m";

const provider = new ethers.providers.JsonRpcProvider('https://rpc.ankr.com/bsc/YOUR-API-KEY');
// const provider = new ethers.providers.WebSocketProvider('wss://rpc.ankr.com/bsc/ws/YOUR-API-KEY');

// Factory V2
const contractAddress = '0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73';
// Factory V2 Contract ABI 
const contractABI = [
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "token0",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "token1",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "address",
        "name": "pair",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "name": "PairCreated",
    "type": "event"
  }
];

const tokenABI = [
  {
    "constant": true,
    "inputs": [],
    "name": "symbol",
    "outputs": [{"name": "", "type": "string"}],
    "type": "function"
  }
];

// Pair contract ABI
const pairABI = [
  {
    "constant": true,
    "inputs": [],
    "name": "getReserves",
    "outputs": [
      { "internalType": "uint112", "name": "_reserve0", "type": "uint112" },
      { "internalType": "uint112", "name": "_reserve1", "type": "uint112" },
      { "internalType": "uint32", "name": "_blockTimestampLast", "type": "uint32" }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  }
];

const contract = new ethers.Contract(contractAddress, contractABI, provider);

contract.on('PairCreated', async (token0, token1, pair) => {
  const token0Contract = new ethers.Contract(token0, tokenABI, provider);
  const token1Contract = new ethers.Contract(token1, tokenABI, provider);
  const pairContract = new ethers.Contract(pair, pairABI, provider);
  
  const symbol0 = await token0Contract.symbol();
  const symbol1 = await token1Contract.symbol();
  const reserves = await pairContract.getReserves();

  const formatReserve0 = ethers.utils.formatUnits(reserves._reserve0, 'ether');
  const formatReserve1 = ethers.utils.formatUnits(reserves._reserve1, 'ether');

  const alertThresholds = {
    "WBNB": 100, //Change your quantity
    "USDT": 50000, //Change your quantity
    "USDC": 50000 //Change your quantity
  };

  if (alertThresholds[symbol0] && Number(formatReserve0) > alertThresholds[symbol0]) {
    playSound.play('Ping.aiff', (err) => {
      if (err) console.log(`Could not play sound: ${err}`);
    });
  }

  if (alertThresholds[symbol1] && Number(formatReserve1) > alertThresholds[symbol1]) {
    playSound.play('Ping.aiff', (err) => {
      if (err) console.log(`Could not play sound: ${err}`);
    });
  }  

  console.log(`${blue}Pool Created: ${pair}${reset}`);
  console.log(`---------------------------------------------------------`);
  console.log(`${green}${symbol0} Address:${reset} ${token0}`);
  console.log(`${green}${symbol1} Address:${reset} ${token1}`);
  console.log(`Reserves (${red}${symbol0})${reset}: ${Number(formatReserve0).toLocaleString('en-US', { maximumFractionDigits: 4 })}`);
  console.log(`Reserves (${red}${symbol1}${reset}): ${Number(formatReserve1).toLocaleString('en-US', { maximumFractionDigits: 4 })}`);
  console.log(`------------------------JOSEPH-TRAN----------------------`);

  
});

console.log("Joseph's listening for new pairs...");

