import jsf from 'json-schema-faker';
import * as fs from 'fs';

let schema = JSON.parse(fs.readFileSync("schemas/transactions.v1.schema.json", "utf8"));
console.log("the schema+>\n", schema)
const syncValue = jsf.generate(schema, {});

console.log(syncValue)

