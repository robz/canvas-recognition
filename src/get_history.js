const PubNub = require('pubnub');
const fs = require('fs');
const keys = require('./keys');

const pubnub = new PubNub(keys);

if (process.argv.length !== 3) {
  console.log('usage: node get_history.js number_of_messages start_date');
  process.exit();
}

const count = Number(process.argv[2]);
console.log(`requesting ${count} messages`);

const filename = `recorded-mistakes/messages-${new Date()
  .toString()
  .replace(/ /g, '_')}.json`;

function save(messages) {
  const data = JSON.stringify(messages, null, '  ');
  const uuidCounts = messages.reduce(
    (a, e) => a.set(e.entry.uuid, 1 + (a.get(e.entry.uuid) || 0)),
    new Map(),
  );
  console.log('uuids:', uuidCounts);
  console.log(`received ${messages.length} total messages`);
  fs.writeFile(filename, data, () => console.log('wrote to ' + filename));
}

function getHistory(count, startTimeToken, allMessages) {
  pubnub.history(
    {
      channel: 'digit_prediction_mistakes',
      count,
      stringifiedTimeToken: true,
      start: startTimeToken,
    },
    (status, response) => {
      console.log(`received ${response.messages.length} messages`);
      allMessages = allMessages.concat(response.messages);

      if (response.messages.length === 100 && count !== 100) {
        getHistory(count - 100, response.startTimeToken, allMessages);
      } else {
        save(allMessages);
      }
    },
  );
}

getHistory(count, null, []);
