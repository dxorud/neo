CREATE TABLE usertbl (
	userid char(8) NOT NULL PRIMARY KEY,
	username nvarchar2(20) NOT NULL,
	birthyear number(4) NOT NULL,
	addr nchar(2) NOT NULL,
	mobile1 char(3),
	mobile2 char(8),
	height number(3),
	mdate	date
);

ALTER TABLE USER1TBL ADD CONSTRAINT user1tbl_pk PRIMARY key(userid);
