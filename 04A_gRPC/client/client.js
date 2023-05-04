const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

const PROTO_PATH = '../proto/stock_exchange.proto';
const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true
});

const stock_exchange_proto = grpc.loadPackageDefinition(packageDefinition).stock_exchange;

const MAX_RETRIES = 5;

function subscribe(client, symbols, attempt = 1) {
    const call = client.Subscribe({ symbols: symbols });
    console.log(`Subscribing to symbols: ${symbols}`);

    call.on('data', (response) => {
        console.log('Received stock data: ', response);
    });

    call.on('end', () => {
        console.log('Server ended call');
    });

    call.on('error', (e) => {
        if (attempt <= MAX_RETRIES) {
            console.log(e);
            console.log(`Attempt ${attempt} failed, retrying...`);
            setTimeout(() => subscribe(client, symbols, attempt + 1), 2000);
        } else {
            console.error('Maximum retries reached, problem with the call', e);
        }
    });
}

function subscribeOnPctChange(client, symbols, pct_change, attempt = 1) {
    console.log(`Subscribing to symbols: ${symbols} with pct_change: ${pct_change}`);
    const call = client.SubscribeOnPctChange({ symbols: symbols, pct_change: pct_change });

    call.on('data', function (response) {
        console.log('Received stock data: ', response);
    });

    call.on('end', function () {
        console.log('Server ended call');
    });

    call.on('error', function (e) {
        if (attempt <= MAX_RETRIES) {
            console.log(e);
            console.log(`Attempt ${attempt} failed, retrying...`);
            setTimeout(() => subscribeOnPctChange(client, symbols, pct_change, attempt + 1), 1000);
        } else {
            console.error('Maximum retries reached, problem with the call', e);
        }
    });
}

function ping(client) {
    client.Ping({}, (error, _) => {
        if (error) {
            console.error('Error pinging server:', error);
        } else {
            console.log('Ping successful');
        }
    });
}

function main() {
    const client = new stock_exchange_proto.StockExchange(
        'localhost:50051',
        grpc.credentials.createInsecure());

    const [subscriptionType, ...args] = process.argv.slice(2);

    if (!subscriptionType || args.length === 0) {
        console.log('Please provide subscription type and arguments');
        console.log('Usage: node client.js <regular | onchange> <args>');
        process.exit(1);
    }

    setInterval(() => ping(client), 10000);

    if (subscriptionType === 'regular') {
        const symbols = args.slice();
        subscribe(client, symbols);
    } else if (subscriptionType === 'onchange') {
        const pct_change = parseFloat(args[0]);
        const symbols = args.slice(1);
        subscribeOnPctChange(client, symbols, pct_change);
    } else {
        console.log('Invalid subscription type');
        process.exit(1);
    }
}

main();
