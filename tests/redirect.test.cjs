const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

const template = fs.readFileSync(path.join(__dirname, '../deploy/aws-stack.yaml'), 'utf8');
const source = template.split('      FunctionCode: |\n')[1].split('\n  Distribution:')[0]
  .split('\n').map(line => line.replace(/^        /, '')).join('\n');
const context = vm.createContext({});
vm.runInContext(source, context);
function request(host, uri = '/', querystring = {}) {
  return { headers: { host: { value: host } }, uri, querystring };
}

test('canonical requests pass through unchanged', () => {
  const original = request('inversionesacc.com', '/img/logo.png');
  assert.equal(context.handler({ request: original }), original);
});
test('www and temporary hosts redirect to the official HTTPS host', () => {
  for (const host of ['www.inversionesacc.com', 'example.cloudfront.net']) {
    const result = context.handler({ request: request(host, '/img/logo.png') });
    assert.equal(result.statusCode, 301);
    assert.equal(result.headers.location.value, 'https://inversionesacc.com/img/logo.png');
  }
});
test('index.html redirects to root', () => {
  const result = context.handler({ request: request('inversionesacc.com', '/index.html') });
  assert.equal(result.headers.location.value, 'https://inversionesacc.com/');
});
test('redirects preserve encoded and repeated campaign parameters', () => {
  const query = { utm_source: { value: 'email%20ACC' }, tag: { multiValue: [{ value: 'a%2Fb' }, { value: 'c' }] } };
  const result = context.handler({ request: request('www.inversionesacc.com', '/', query) });
  assert.equal(result.headers.location.value, 'https://inversionesacc.com/?utm_source=email%20ACC&tag=a%2Fb&tag=c');
});
