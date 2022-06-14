'use strict';
const Database = require('../.');

describe('Database#cipher_fts()', function () {
	beforeEach(function () {
		this.db = new Database(util.next());
	});
	afterEach(function () {
		this.db.close();
	});
	
	it('cipher key', function () {
		let rows = this.db.pragma(`key = '123'`);
		rows = this.db.pragma(`rekey = '456'`);
		const r1 = this.db.exec('CREATE TABLE entries (a TEXT, b INTEGER)');
		const r2 = this.db.exec("INSERT INTO entries VALUES ('foobar', 44); INSERT INTO entries VALUES ('baz', NULL);");
		const r3 = this.db.exec('SELECT * FROM entries');
		const r4 = this.db.exec(`CREATE VIRTUAL TABLE t1 USING fts3(text, tokenize='mmicu')`);
		const r5 = this.db.exec("INSERT INTO t1 VALUES ('foobar'); INSERT INTO t1 VALUES ('baz');");

		expect(r1).to.equal(this.db);
		expect(r2).to.equal(this.db);
		expect(r3).to.equal(this.db);
		expect(r4).to.equal(this.db);
		expect(r5).to.equal(this.db);

	});
});
