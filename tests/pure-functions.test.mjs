import { test } from 'node:test';
import assert from 'node:assert/strict';
import { sanitize, timingSafeEqual, ipHash } from '../src/index.ts';

test('timingSafeEqual: identical strings match', () => {
  assert.equal(timingSafeEqual('a-real-secret-key', 'a-real-secret-key'), true);
});

test('timingSafeEqual: different values of equal length do not match', () => {
  assert.equal(timingSafeEqual('a-real-secret-key', 'a-fake-secret-key'), false);
});

test('timingSafeEqual: different-length values do not match', () => {
  assert.equal(timingSafeEqual('short', 'a-much-longer-value'), false);
});

test('timingSafeEqual: case-sensitive', () => {
  assert.equal(timingSafeEqual('Secret', 'secret'), false);
});

test('sanitize: strips control characters and trims', () => {
  assert.equal(sanitize('  hello\x00world\x1F  '), 'helloworld');
});

test('sanitize: null/undefined become empty string', () => {
  assert.equal(sanitize(null), '');
  assert.equal(sanitize(undefined), '');
});

test('sanitize: truncates to max length', () => {
  assert.equal(sanitize('abcdefgh', 4), 'abcd');
});

test('ipHash: is deterministic for the same input', () => {
  assert.equal(ipHash('203.0.113.5'), ipHash('203.0.113.5'));
});

test('ipHash: differs for different inputs', () => {
  assert.notEqual(ipHash('203.0.113.5'), ipHash('203.0.113.6'));
});
