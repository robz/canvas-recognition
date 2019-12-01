const PubNub = require('pubnub');
const fs = require('fs');
const keys = require('./keys');

const pubnub = new PubNub(keys);

if (process.argv.length !== 3) {
  console.log('usage: node get_history.js number_of_messages');
  process.exit();
}

const count = Number(process.argv[2]);
console.log(`requesting ${count} messages`);

pubnub.history(
  {
    channel: 'digit_prediction_mistakes',
    count,
    stringifiedTimeToken: true,
  },
  (status, response) => {
    const data = JSON.stringify(response.messages, null, '  ');

    const uuidCounts = response.messages.reduce(
      (a, e) => a.set(e.entry.uuid, 1 + (a.get(e.entry.uuid) || 0)),
      new Map(),
    );
    console.log('uuids:', uuidCounts);

    console.log(`received ${response.messages.length} responses`);
    const filename = `recorded-mistakes/messages-${new Date()
      .toString()
      .replace(/ /g, '_')}.json`;

    fs.writeFile(filename, data, () => console.log('wrote to ' + filename));
  },
);
